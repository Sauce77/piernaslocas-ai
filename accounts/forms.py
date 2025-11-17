from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )