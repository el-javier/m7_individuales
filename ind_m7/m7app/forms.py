from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Tarea


class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ('titulo', 'descripcion', 'fecha_vencimiento', 'estado', 'etiqueta')
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class ObservacionForm(forms.Form):
    observacion = forms.CharField(widget=forms.Textarea)
