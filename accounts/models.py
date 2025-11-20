from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contacto(models.Model):

    OPCIONES_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    OPCIONES_PERFIL = [
        ('T', 'Terapeuta'),
        ('U', 'Usuario'),
    ]

    sexo = models.CharField(max_length=1, choices=OPCIONES_SEXO, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    contacto_emergencia = models.CharField(max_length=10, null=False, blank=False)
    perfil =  models.CharField(max_length=1, choices=OPCIONES_PERFIL, null=False, blank=False, default='U')
    cedula_profesional = models.CharField(max_length=10, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"
    