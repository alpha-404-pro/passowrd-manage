from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import PasswordEntry
from .forms import LoginForm, PasswordEntryForm
import secrets
import string
import json
from django.contrib.auth import logout
from django.shortcuts import redirect

# Add this new view
def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'passwords': passwords})

@login_required
def add_password(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Password saved successfully!')
            return redirect('dashboard')
    else:
        form = PasswordEntryForm()
    
    return render(request, 'add_password.html', {'form': form})

@login_required
def edit_password(request, pk):
    password_entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=password_entry)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Password updated successfully!')
            return redirect('dashboard')
    else:
        form = PasswordEntryForm(instance=password_entry)
        form.initial['password'] = password_entry.get_password()
    
    return render(request, 'edit_password.html', {'form': form, 'password_entry': password_entry})

@login_required
def delete_password(request, pk):
    password_entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        password_entry.delete()
        messages.success(request, 'Password deleted successfully!')
    return redirect('dashboard')

@login_required
def generate_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        length = int(data.get('length', 12))
        
        # Generate random password
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        return JsonResponse({'password': password})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_password(request, pk):
    password_entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    return JsonResponse({'password': password_entry.get_password()})
