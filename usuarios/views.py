from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from reciclaje.models import User
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
       elif curp is '' and password is '':
            messages.success(request, ("CURP y Contraseña no valida"))
            return redirect('login')
       elif curp is '':
            messages.success(request, ("CURP no valida"))
            return redirect('login')
       elif password is '':
            messages.success(request, ("Contraseña no valida"))
            return redirect('login')
       else:
            messages.success(request, ("Credenciales incorrectas"))
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
                    Group.objects.get_or_create(name = 'Habitantes')
                    group = Group.objects.get(name='Habitantes')
                    user.groups.add(group)
                    content_type = ContentType.objects.get_for_model(User)
                    Group.objects.get_or_create(name = 'Recolector')
                    group_r = Group.objects.get(name='Recolector')
                    recolector = Permission.objects.get(codename= 'recolector',  content_type= content_type)
                    group_r.permissions.add(recolector)
                    Group.objects.get_or_create(name = 'Canjeador')
                    group_c = Group.objects.get(name='Canjeador')
                    canjeador = Permission.objects.get('canjeador')
                    canjeador = Permission.objects.get(codename= 'canjeador',  content_type= content_type)
                    group_c.permissions.add(canjeador)
                    login(request, user)
                    messages.success(request, ("Registro Exitoso!"))
                    return redirect('homee')
               else:
                    if total_gruops[0].name == 'Habitantes':
                         group = Group.objects.get(name='Habitantes')
                         user.groups.add(group)
                         login(request, user)
                         messages.success(request, ("Registro Exitoso!"))
                         return redirect('homee')
                    else:
                         Group.objects.get_or_create(name = 'Habitantes')
                         login(request, user)
                         messages.success(request, ("Registro Exitoso!"))
                         return redirect('homee')

     else:
          form = CustomUserCreationForm()
     return render(request, 'authenticate/register_user.html', {
          'form':form
     })


     

