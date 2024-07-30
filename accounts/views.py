# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserSignupForm, UserLoginForm
from .models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard')  # Redirect to the dashboard or another page
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

def dashboard(request):
    user = request.user
    return render(request, 'dashboard.html', {'user': user})
