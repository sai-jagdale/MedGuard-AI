from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# --- Image Upload Form (UPDATED) ---
class ImageUploadForm(forms.Form):
    # 1. Text search input (remains the same)
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Search for medicine by name...', # Updated placeholder
            'id': 'search_query' 
        })
    )
    
    # 2. NEW: Packaging Image input (for OCR Agent)
    packaging_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'sr-only', 
            'id': 'packaging_upload', # New ID
            'accept': 'image/png, image/jpeg, image/jpg'
        })
    )

    # 3. NEW: Barcode Image input (for Barcode Agent)
    barcode_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'sr-only', 
            'id': 'barcode_upload', # New ID
            'accept': 'image/png, image/jpeg, image/jpg'
        })
    )

    # --- UPDATED VALIDATION METHOD ---
    def clean(self):
        cleaned_data = super().clean()
        search_query = cleaned_data.get("search_query")
        packaging_image = cleaned_data.get("packaging_image")
        barcode_image = cleaned_data.get("barcode_image")
        
        # Strip whitespace from search query
        search_query_stripped = search_query.strip() if search_query else ""

        # Enforce that AT LEAST ONE of the three fields is provided
        if not packaging_image and not barcode_image and not search_query_stripped:
            raise forms.ValidationError(
                "Please enter a medicine name, upload a packaging image, or upload a barcode image to start."
            )
        
        # Update the cleaned data with the stripped query
        cleaned_data['search_query'] = search_query_stripped
        
        return cleaned_data

# --- Signup Form (UNCHANGED) ---
class NewUserForm(UserCreationForm):
    # Add the extra fields we want
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')