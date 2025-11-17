from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contacto(models.Model):

    OPCIONES_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino')
    ]
    
    sexo = models.CharField(max_length=1, choices=OPCIONES_SEXO, required=True, null=False, blank=False)
    fecha_nacimiento = models.DateField(required=True, null=False, blank=False)
    contacto_emergencia = models.CharField(max_length=10, required=True, null=False, blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"