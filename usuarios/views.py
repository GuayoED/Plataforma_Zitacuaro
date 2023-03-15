from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomEscuelaCreationForm
from django.contrib.auth.models import Group, Permission

def login_user(request):
    if request.method == "POST":
       curp = request.POST['curp']
       password = request.POST['password']
       user = authenticate(request, username=curp, password=password)
       if user is not None:
            login(request, user)
            return redirect('homee')
       else:
            messages.success(request, ("Ocurrio un error al iniciar sesion, intenta de nuevo... "))
            return redirect('login')
    
    else:
        return render(request, 'authenticate/login.html', {})
    

def logout_user(request):
     logout(request)
     messages.success(request, ("Has cerrado tu sesion!"))
     return redirect('login')


def register_escuela(request):
     if request.method == "POST":
          form = CustomEscuelaCreationForm(request.POST)
          print("aqui")
          if form.is_valid():
               form.save()
               clave = form.cleaned_data['CURP']
               password = form.cleaned_data['password1']
               user = authenticate(username=clave, password=password)
               total_gruops = Group.objects.all()
               if len(total_gruops) == 0:
                    Group.objects.get_or_create(name = 'escuelas')
                    group = Group.objects.get(name='escuelas')
                    user.groups.add(group)
                    user.is_active = False
                    user.save()
                    messages.success(request, ("Registro Exitoso!"))
                    return redirect('homee')
               else:
                    if total_gruops[0].name == 'escuelas':
                         group = Group.objects.get(name='escuelas')
                         user.groups.add(group)
                         user.is_active = False
                         user.save()
                         messages.success(request, ("Registro Exitoso!"))
                         return redirect('homee')
                    else:
                         Group.objects.get_or_create(name = 'escuelas')
                         group = Group.objects.get(name='escuelas')
                         user.groups.add(group)
                         user.is_active = False
                         user.save()
                         messages.success(request, ("Registro Exitoso!"))
                         return redirect('homee')
     else:
          form = CustomEscuelaCreationForm()
     return render(request, 'authenticate/regis_escuela.html', {
          'form':form
     })

def register_user(request):
     if request.method == "POST":
          form = CustomUserCreationForm(request.POST)
          if form.is_valid():
               form.save()
               curp = form.cleaned_data['CURP']
               password = form.cleaned_data['password1']
               user = authenticate(username=curp, password=password)
               total_gruops = Group.objects.all()
               if len(total_gruops) == 0:
                    Group.objects.get_or_create(name = 'habitantes')
                    group = Group.objects.get(name='habitantes')
                    user.groups.add(group)
                    login(request, user)
                    messages.success(request, ("Registro Exitoso!"))
                    return redirect('homee')
               else:
                    if total_gruops[0].name == 'habitantes':
                         group = Group.objects.get(name='habitantes')
                         user.groups.add(group)
                         login(request, user)
                         messages.success(request, ("Registro Exitoso!"))
                         return redirect('homee')
                    else:
                         Group.objects.get_or_create(name = 'habitantes')

     else:
          form = CustomUserCreationForm()
     return render(request, 'authenticate/register_user.html', {
          'form':form
     })


     

