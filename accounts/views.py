from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def home(request):
    return HttpResponse("Mia Khalifa")

def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Autenticar al usuario
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Si la autenticación es exitosa, iniciamos sesión
                login(request, user)
                # Opcionalmente, mostrar un mensaje de éxito
                messages.success(request, f'¡Bienvenido/a de nuevo, {username}!')
                return redirect('home')
            else:
                # Si la autenticación falla (credenciales incorrectas)
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                # Mantenemos el formulario en la página con el error
                return render(request, 'login.html', {'form': form})
    else:
        # Petición GET: Mostramos un formulario vacío
        form = LoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})

# Create your views here.
