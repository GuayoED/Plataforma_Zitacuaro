from django import forms
from reciclaje.models import User
from django.contrib.auth.forms import UserCreationForm


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class CustomUserCreationForm(UserCreationForm):
    CURP = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'minlength':'18' , 'maxlength':'18'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'}))
    #username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    fechaNacimiento = forms.DateField(widget=DateTimeInput(attrs={'class':'form-control form-control-lg'}))
    

    class Meta:
        model = User

        #fields = "__all__"
        fields = ['CURP', 'first_name', 'last_name', 'email', 'fechaNacimiento', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'



class CustomEscuelaCreationForm(UserCreationForm):
    CURP = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'}))
    #username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    class Meta:
        model = User

        #fields = "__all__"
        fields = ['CURP', 'first_name','email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomEscuelaCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'