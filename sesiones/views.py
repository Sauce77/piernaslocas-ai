from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Historial, Rutina
# Create your views here.

@login_required
def mostrar_historial(request, username):

    # obtenemos el usuario
    usuario = get_object_or_404(User, username=username)

    try:
        # obtenemos el historial
        historial = Historial.objects.get(paciente=usuario)
        # obtenemos las rutinas
        rutinas = Rutina.objects.filter(historial=historial)
    except Historial.DoesNotExist:
        historial = None
        rutinas = None

    contexto = {
        "usuario": usuario,
        "historial": historial,
        "rutinas": rutinas,
    }

    return render(request, "sesiones/historial.html", contexto)

@login_required
def mostar_rutinas(request):

    try:
        # obtenemos el historial
        historial = Historial.objects.get(paciente=request.user)
        # obtenemos las rutinas
        rutinas = Rutina.objects.filter(historial=historial)
    except Historial.DoesNotExist:
        historial = None
        rutinas = None

    contexto = {
        "historial": historial,
        "rutinas": rutinas,
    }

    return render(request, "sesiones/rutinas.html", contexto)