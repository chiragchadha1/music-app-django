from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

# User Registration
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email')  # Optional

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login(request, user)
        return redirect('home')  # Redirect to a home page or another appropriate page

    return render(request, 'register.html')  # Path to your registration template

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or another appropriate page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')  # Path to your login template

