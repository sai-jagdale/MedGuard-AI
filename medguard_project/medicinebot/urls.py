# medicinebot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This one path handles both showing the home page and processing the form
    path('', views.home_view, name='home'), # <-- This name is now corrected
    
    # Auth paths
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Account/History path
    path('account/', views.account_view, name='account'), # <-- This name is now corrected

]

