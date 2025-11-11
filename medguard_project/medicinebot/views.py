import base64
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Local imports
from .forms import ImageUploadForm, NewUserForm
from .models import History
from .agents.barcode_agent import run_barcode_agent
from .agents.ocr_agent import run_ocr_agent
from .agents.extraction_agent import run_extraction_agent
from .agents.search_agent import run_search_agent
from .agents.summary_agent import run_summary_agent


@login_required
def home_view(request):
    """
    Handles both displaying the form (GET) and processing the search/upload (POST).
    """
    context = {'form': ImageUploadForm()} # Start with a fresh form

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the 3 distinct inputs from the new form
            search_query_input = form.cleaned_data.get('search_query')
            packaging_image = form.cleaned_data.get('packaging_image')
            barcode_image = form.cleaned_data.get('barcode_image')

            image_data_url = None
            analysis_summary = None
            final_search_query_for_history = None
            is_barcode_search = False
            search_query_for_agents = None
            extracted_data = {}

            try:
                # --- NEW 3-PATH LOGIC ---
                
                if barcode_image:
                    # --- PATH A: BARCODE IMAGE UPLOADED (Exact Match) ---
                    is_barcode_search = True
                    
                    # 1. Prepare image for display
                    image_file = barcode_image
                    image_file.seek(0)
                    image_bytes = image_file.read()
                    image_data_url = f"data:{image_file.content_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    image_file.seek(0) 

                    # 2. Run BARCODE AGENT ONLY
                    barcode_data = run_barcode_agent(image_file)
                    
                    if barcode_data:
                        search_query_for_agents = barcode_data
                        final_search_query_for_history = f"Barcode Scan: {barcode_data}"
                        extracted_data = {
                            'Name': f"Barcode: {barcode_data}", 
                            'MFG Date': 'Not Found', 'Expiry Date': 'Not Found',
                            'MRP': 'Not Found', 'Is Expired': False
                        }
                    else:
                        messages.error(request, 'Barcode not recognized. Please use a clearer picture.')
                        return render(request, 'medicinebot/home.html', context)

                elif packaging_image:
                    # --- PATH B: PACKAGING IMAGE UPLOADED (OCR/Fuzzy Match) ---
                    is_barcode_search = False

                    # 1. Prepare image for display
                    image_file = packaging_image
                    image_file.seek(0)
                    image_bytes = image_file.read()
                    image_data_url = f"data:{image_file.content_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    image_file.seek(0)

                    # 2. Run OCR/EXTRACTION AGENTS ONLY
                    raw_text = run_ocr_agent(image_file)
                    if not raw_text:
                        messages.error(request, 'OCR failed. Could not read text from image. Please use a clearer picture.')
                        return render(request, 'medicinebot/home.html', context)

                    extracted_data = run_extraction_agent(raw_text)
                    search_query_for_agents = extracted_data.get('Name', raw_text)
                    final_search_query_for_history = extracted_data.get('Name', raw_text).strip()

                elif search_query_input:
                    # --- PATH C: TEXT SEARCH (Fuzzy Match) ---
                    is_barcode_search = False
                    search_query_for_agents = search_query_input
                    extracted_data = {
                        'Name': search_query_input,
                        'MFG Date': 'Not Applicable', 'Expiry Date': 'Not Applicable',
                        'MRP': 'Not Applicable', 'Is Expired': False
                    }
                    final_search_query_for_history = search_query_input

                else:
                    # This case should be caught by form.clean(), but as a fallback:
                    messages.error(request, 'Please submit a query or an image.')
                    return render(request, 'medicinebot/home.html', context)

                # --- Run common agents (Search and Summary) ---
                
                # is_barcode_search flag is now correctly set by the logic above
                search_results = run_search_agent(search_query_for_agents, is_barcode=is_barcode_search)
                
                analysis_summary = run_summary_agent(search_results, extracted_data, is_barcode=is_barcode_search)

                # --- Save to History ---
                if final_search_query_for_history or analysis_summary:
                    History.objects.create(
                        user=request.user,
                        search_query=final_search_query_for_history,
                        analysis_summary=analysis_summary,
                        image_data_url=image_data_url
                    )
                else:
                    messages.warning(request, "Search did not yield results to save.")

                # Pass results to the template
                context['analysis_summary'] = analysis_summary
                context['image_data_url'] = image_data_url

            except Exception as e:
                messages.error(request, f"An unexpected error occurred during analysis: {e}")
                
            context['form'] = form 
                
        else:
            context['form'] = form 
            messages.error(request, 'Please correct the errors below.')

    # Render the page (for GET requests or after POST processing)
    return render(request, 'medicinebot/home.html', context)


# ----------------------------------------------------------------------
# --- AUTHENTICATION VIEWS (Unchanged) ---------------------------------
# ----------------------------------------------------------------------


@login_required
def account_view(request):
    """
    Displays the user's search history.
    """
    history_list = History.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        'history_list': history_list
    }
    return render(request, 'medicinebot/account-history.html', context)


def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {username}!")
                next_page = request.POST.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('home') 
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'next': request.GET.get('next', '')
    }
    return render(request, 'medicinebot/login.html', context)


def signup_view(request):
    """
    Handles new user registration.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            pass
    else:
        form = NewUserForm()

    return render(request, 'medicinebot/signup.html', {'form': form})


def logout_view(request):
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')