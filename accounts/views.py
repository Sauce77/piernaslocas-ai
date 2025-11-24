from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, ContactoForm
import datetime

def home(request):
    return render(request, "accounts/index.html")

def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('accounts:home')
        
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
                return redirect('accounts:home')
            else:
                # Si la autenticación falla (credenciales incorrectas)
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                # Mantenemos el formulario en la página con el error
                return render(request, 'accounts/login.html', {'form': form})
    else:
        # Petición GET: Mostramos un formulario vacío
        form = LoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):

    if request.method == 'POST':

        # ingresamos las respuestas al form de usuario
        user_form = SignupForm(request.POST)

        # ingresamos las respuestas al form de contacto
        contacto_form = ContactoForm(request.POST)

        # si la informacion de usuario y contacto es valida
        if user_form.is_valid() and contacto_form.is_valid():

            # guardamos la informacion del usuario
            user = user_form.save()

            # creamos una instancia del contacto
            contacto = contacto_form.save(commit=False)
            contacto.user = user
            contacto.save()

            messages.success(request, f'Cuenta creada exitosamente para {user.username}. ¡Ahora puedes iniciar sesión!')
            return redirect('accounts:login')
    
    else:

        user_form = SignupForm()
        contacto_form = ContactoForm()

        # Iterar sobre los campos para añadir la clase 'form-control'
        for field in user_form.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        for field in contacto_form.fields.values():
            field.widget.attrs['class'] = 'form-control'

    contexto = {
        "user_form": user_form,
        "contacto_form": contacto_form,
    }

    return render(request, "accounts/signup.html", contexto)

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:home')

@login_required
def profile_view(request, username):
    """
        Muestra la informacion del usuario seleccionado.
    """

    # obtenemos el objeto usuario
    usuario = get_object_or_404(User, username=username)
    edad = None

    if hasattr(usuario, "contacto"):
        # calculamos la edad a partir de la fecha nacimiento
        hoy = datetime.datetime.today()
        fecha_nacimiento = usuario.contacto.fecha_nacimiento
        edad = hoy.year - fecha_nacimiento.year

        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1


    contexto = {
        "usuario": usuario,
        "edad": edad,
    }

    return render(request, "accounts/perfil.html", contexto)