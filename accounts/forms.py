from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Contacto

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'class': ' form-control w-100'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100'})
    )

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):

        fields = ('username', 'email', 'first_name', 'last_name')



class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        exclude = ['user', 'cedula_profesional']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }