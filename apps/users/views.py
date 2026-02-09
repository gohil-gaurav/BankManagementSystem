from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm


def home_view(request):
    """
    Home/Landing Page View
    - Shows welcome page with login/register options
    """
    if request.user.is_authenticated:
        # If already logged in, redirect to appropriate dashboard
        if hasattr(request.user, 'manager_profile'):
            return redirect('bank:manager_dashboard')
        else:
            return redirect('bank:dashboard')
    
    return render(request, 'home.html')


def register_view(request):
    """
    User Registration View
    - GET: Show registration form
    - POST: Process registration, create user + account, login, redirect to dashboard
    """
    if request.user.is_authenticated:
        # If already logged in, redirect to dashboard
        return redirect('bank:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Save the user
            user = form.save()
            
            # Account is automatically created via signal!
            
            # Log the user in
            login(request, user)
            
            # Show success message
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            
            # Redirect to dashboard
            return redirect('bank:dashboard')
        else:
            # Form has errors, they'll be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show empty form
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    User Login View
    - GET: Show login form
    - POST: Authenticate user, login, redirect to dashboard
    """
    if request.user.is_authenticated:
        # If already logged in, redirect to dashboard
        return redirect('bank:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Get username and password from form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Login the user
                login(request, user)
                
                # Show success message
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to dashboard
                return redirect('bank:dashboard')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
    else:
        # GET request - show empty form
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    User Logout View
    - Logs out the user and redirects to home page
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:home')
