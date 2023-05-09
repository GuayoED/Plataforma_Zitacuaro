from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Entradas, Premio_usuario
 

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'pic']


class EntradasForm(ModelForm):
    
    class Meta:
        model = Entradas
        fields= [ "Curp", "DF", "Cantidad"]
        widgets = {
            'Curp': forms.TextInput(
                attrs={
                    'data-url': '/search/',
                    'id': "search-input",
                    'name': "q"
                }
            )
        }

class RecompensasForm(ModelForm):

    class Meta:
        model = Premio_usuario
        fields = "__all__"

        widgets = {
            'usuario': forms.TextInput(
                attrs={
                    'data-url': '/search/',
                    'id': "search-input",
                    'name': "q"
                }
            )
        }



