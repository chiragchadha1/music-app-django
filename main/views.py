from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

# User Registration
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('main:register')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        user.save()
        login(request, user)
        return redirect('main:home')  # Redirect to a home page or another appropriate page

    return render(request, 'register.html')  # Path to your registration template

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')  # Redirect to a home page or another appropriate page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')  # Path to your login template

def logout_view(request):
    logout(request)
    # Redirect to a success page, home page, or login page after logout
    return redirect('main:home')  # Replace 'home' with the name of the view you want to redirect to
