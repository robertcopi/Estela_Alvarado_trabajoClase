from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Perfil

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    # Ensure profile exists
    if not hasattr(request.user, 'perfil'):
        Perfil.objects.create(user=request.user)
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name', '').strip()
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0] if len(name_parts) > 0 else ''
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.email = request.POST.get('email', '')
        user.save()
        
        perfil, created = Perfil.objects.get_or_create(user=user)
        perfil.mobile = request.POST.get('mobile', '')
        perfil.save()
        
        messages.success(request, 'Perfil actualizado correctamente.')
    return redirect('profile')
