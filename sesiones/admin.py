from django.contrib import admin

from .models import Ejercicio, Rutina, Historial
# Register your models here.
admin.site.register(Ejercicio)
admin.site.register(Rutina)
admin.site.register(Historial)