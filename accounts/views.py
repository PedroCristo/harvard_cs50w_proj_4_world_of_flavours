from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import CustomRegistrationForm, CustomLoginForm, UserProfileForm
from django.contrib.auth import get_user_model
from .models import UserProfile

@login_required
def profile(request):
    """
    Render the user profile page, allowing the user to update their information
    """
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            # Save the profile
            form.save()
            # Update the user's email
            new_email = form.cleaned_data.get('email')
            if new_email and new_email != request.user.email:
                request.user.email = new_email
                request.user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    return render(request, 'accounts/user-profile.html', {
        'form': form,
        'user_profile': user_profile
    })


def public_profile(request, username):
    """
    Render the public profile page of a user.
    """
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    context = {
        'user_profile': user_profile,
        'public_profile': True
    }

    return render(request, 'accounts/user-profile.html', context)

                 
def register(request):
    """
    Render the registration page and handle the registration process
    """
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user and save it
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! \
            Your account has been created successfully.')
            return redirect(reverse("home_page"))
        else:
            # If the form is invalid, render the form with error messages
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, "accounts/register.html", {"form": form})
    else:
        # If the request is GET, instantiate an empty form
        form = CustomRegistrationForm()
        return render(request, "accounts/register.html", {"form": form})
    
    
def login_view(request):
    """
    Render the login page
    """
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}! \
                                 You have been successfully logged in.")
                return redirect('home_page')  # Redirect to a success page.
            else:
                # Invalid login credentials
                messages.error(request, 'Invalid username or password\
                                         . Please try again.')
                return render(request, 'accounts/login.html', {'form': form})
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Render the logout page
    """
    user = request.user  
    logout(request)
    if user.is_authenticated:
        messages.success(request, f"You have been successfully \
                                  logged out. See you soon, {user.username}!")
    return HttpResponseRedirect(reverse("home_page"))