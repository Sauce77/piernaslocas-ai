from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ejercicio(models.Model):

    nombre = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    data = models.JSONField()

    def __str__(self):
        return self.nombre

class Historial(models.Model):

    folio = models.CharField(max_length=100, null=False, blank=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    terapeuta = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='historial_terapeuta')
    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='historial_paciente')

    def __str__(self):
        return self.folio
    
class Rutina(models.Model):

    OPCIONES_ESTADO = [
        ('T', 'Terminado'),
        ('P', 'Pendiente'),
        ('C', 'Cancelado'),
    ]

    nombre = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=1, choices=OPCIONES_ESTADO, null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    ejercicios = models.ManyToManyField(Ejercicio)
    historial = models.ForeignKey(Historial, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre