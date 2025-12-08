from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import Historial
# Create your views here.

def mostrar_historial(request, username):

    # obtenemos el usuario
    usuario = get_object_or_404(User, username=username)

    # obtenemos el historial
    historial = Historial.objects.get(paciente=usuario)

    contexto = {
        "usuario": usuario,
        "historial": historial,
    }

    return render(request, "sesiones/historial.html", contexto)