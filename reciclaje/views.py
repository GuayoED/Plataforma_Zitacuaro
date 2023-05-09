from typing import Any, Dict
from django.shortcuts import render, redirect
#Instanciamos las vistas generiaca de Django
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView , DeleteView
#Instanciamos los modelos
from .models import User , Premio, DispoFinal, Premio_usuario, PuntosReciclaje, Entradas, Trabajador, Descuentos 

#Sirve para hacer un reverse
from django.urls import reverse, reverse_lazy
#Maneja los permisos
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# Vista para cambiar la contraseña
from django.contrib.auth.views import PasswordChangeView
#Para usar mensajes Django
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#Para usar formularios
from .forms import UpdateUserForm, EntradasForm, RecompensasForm
#Se importa los grupos
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse


def home(request):
    
    return render(request, 'reciclaje/home.html')



##CRUD DE USUARIOS


class UsuarioList(ListView ):
    model = User
    context_object_name = 'usuario'
    paginate_by = 35


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.request.GET.get("buscar")
        if queryset:
            resultado = User.objects.filter(
                Q(CURP__icontains = queryset) |
                Q(first_name__icontains = queryset) |
                Q(last_name__icontains = queryset)
            ).distinct()
            context['object_list'] = resultado
        #print(context)

        ##### CHECK DE QUIEN ES TRABAJADOR
        Trabajadores = Trabajador.objects.all()
        lista_trabajador = []
        for trabajador in Trabajadores:
            lista_trabajador.append(str(trabajador.trbajador))
        context['lista_trabajadores'] = lista_trabajador
        context['trabajador'] = Trabajadores
        return context


    def has_permission(self):
        users = self.request.user
        return users.has_perm('reciclaje.recolector') or users.has_perm('reciclaje.recolector')


class UsuarioCreate( PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'reciclaje.admin'
    model = User
    form = User
    fields = "__all__"
    success_message = 'Usuario Creado Correctamente'

    def get_success_url(self):
        return reverse('leerUsuarios')
        

class UsuarioDetalle(PermissionRequiredMixin, DetailView):
    model = User

    def has_permission(self):
        users = self.request.user
        return users.has_perm('reciclaje.recolector') or users.has_perm('reciclaje.canjeador')

class UsuarioActulizar( PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'reciclaje.admin'
    model = User
    form = User
    fields = ['CURP', 'first_name', 'last_name', 'email', 'fechaNacimiento', 'puntos', 'groups', 'is_active' ]
    success_message = 'Usuario Actualizado Correctamente'

    def get_success_url(self):
        grupo = Group.objects.filter(user = self.object)
        trabajador = Trabajador.objects.filter(trbajador = self.object)
        if grupo[0].name == 'recolector':
            if len(trabajador) == 0:
                lugar = PuntosReciclaje.objects.all()
                if len(lugar) != 0:
                    t = Trabajador(trbajador=self.object,lugar=lugar[0], id =self.object.id)
                    t.save()
                    t_id = Trabajador.objects.get(trbajador = self.object)
                    return reverse('trabajador', args = [t_id.pk])###AQUI REENVIAR A CREAR TREBAJADOR
                else:
                    success_message = 'No se tiene ningun punto de reciclaje registrado'
                    messages.success (self.request, (success_message))
                    return reverse('leerUsuarios')
            else:
                return reverse('leerUsuarios') ### Ya esta registrado como trbajador
        else:
            return reverse('leerUsuarios')

class UsuarioEliminar(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'reciclaje.admin'
    model = User
    form = User
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Usuario Elminado Correctamente'
        messages.success (self.request, (success_message))
        return reverse('leerUsuarios')

## CRUD DE RECOMPENSAS

class RecompensasList( ListView):
    model = Premio
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.request.GET.get("buscar")
        if queryset:
            resultado = Premio.objects.filter(
                Q(nombre__icontains = queryset) 
            ).distinct()
            context['object_list'] = resultado
        return context

class RecompensasCreate( PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'reciclaje.admin'
    model = Premio
    form = Premio
    fields = "__all__"
    success_message = 'Premio creado correctamente'

    def get_success_url(self):
        return reverse('leerPremios')

class RecompensasDetalle(PermissionRequiredMixin, DetailView):
    permission_required = 'reciclaje.admin'
    model = Premio


class RecompensasActulizar( PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'reciclaje.admin'
    model = Premio
    form = Premio
    fields = "__all__"
    success_message = 'Premio Actualizado Correctamente'

    def get_success_url(self):
        return reverse('leerPremios')

class RecompensasEliminar(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'reciclaje.admin'
    model = Premio
    form = Premio
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Premio Elminado Correctamente'
        messages.success (self.request, (success_message))
        return reverse('leerPremios')


## CRUD DE RECICLAJE
class DispoFinallist(PermissionRequiredMixin, ListView):
    permission_required = 'reciclaje.admin'
    model = DispoFinal
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.request.GET.get("buscar")
        if queryset:
            resultado = DispoFinal.objects.filter(
                Q(nombre__icontains = queryset) 
            ).distinct()
            context['object_list'] = resultado
        return context

class DispoFinalDetalle(PermissionRequiredMixin, DetailView):
    permission_required = 'reciclaje.admin'
    model = DispoFinal

class DispoFinalCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'reciclaje.admin'
    model = DispoFinal
    form = DispoFinal
    fields = "__all__"
    success_message = "Dispocisión final Creada correctamente"
    
    def get_success_url(self):
        return reverse ('leerDispoFinal')


class DispoFinalActualizar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'reciclaje.admin'
    model = DispoFinal
    form = DispoFinal
    fields = "__all__"
    success_message = "Dispocisión final Actualizado correctamente"

    def get_success_url(self):
        return reverse ('leerDispoFinal')

class DispoFinalDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'reciclaje.admin'
    model = DispoFinal
    form = DispoFinal
    fields = "__all__"
    

    def get_success_url(self):
        success_message = "Dispocisión final Eliminada correctamente"
        messages.success (self.request, (success_message))
        return reverse ('leerDispoFinal')


class Equivalencia(ListView):
    model = DispoFinal

##CRUD DE RECOMPENSAS DE USUARIO


class RecompensasUsuarioCreate(SuccessMessageMixin, CreateView):
    model = Premio_usuario
    form_class = RecompensasForm
    #form = Premio_usuario
    #fields = "__all__"
    

    def get_success_url(self):
        ## Faltan validaciones de 0 ##
        preu = Premio_usuario.objects.all() ##Se obtienen todos los objetos
        longitud = len(preu)  ## Se saca la longitud del arreglo de arriba
        pu = preu[longitud-1] ## Se saca la ultima poosicion creada
        re = pu.premio.nombre ## Se obtienen el nombre del premio
        cos = pu.premio.valor ## Se obtiene el valor del premio
        usu = pu.usuario.puntos ## Se obtiene los puntos de usuario
        if( usu > cos):  ## Se ve si el usu tiene puntos suficientes y se baja el stock de producto
            prem = Premio.objects.get(nombre=re)
            prem.stock = prem.stock - 1
            pu.usuario.puntos = pu.usuario.puntos - prem.valor
            pu.usuario.save()
            prem.save()
            success_message = "Premio canjeado correctamente"
            messages.success (self.request, (success_message))
            return reverse ('detallesUsuario', args = [pu.usuario.pk])
        else:               ## Si no se elimina el producto canjeado
            pu.delete()
            success_message = "El usuario no cuenta con los puntos suficientes"
            messages.success (self.request, (success_message))
            return reverse('detallesUsuario', args = [pu.usuario.pk])
        
    def post(self, request, *args, **kwarg):
        _mutaable = self.request.POST._mutable
        self.request.POST._mutable = True
        usu = self.request.POST['usuario']
        result = User.objects.get(CURP=usu)
        self.request.POST['usuario'] = result.pk
        return super().post(request, *args, **kwarg)
    


## BARRA DE BUSQUEDA ##
    
def buscar_productos(request):
    if request.method == "POST":
        buscar = request.POST['buscar']
        producto = Premio.objects.filter(nombre__contains=buscar)
        return render(request, 'reciclaje/catalogob.html', {'buscar':buscar, 'producto':producto})
    else:
        return render(request, 'reciclaje/catalogob.html')
    

def ver_productos(requst):
    usere =  requst.user.CURP
    premio = Premio_usuario.objects.all()
    list=[]
    for x in premio:
        if str(x.usuario) == usere:
            list.append(x)

    

    #premio_u = Premio_usuario.objects.filter(usuario__contains=usere)

    return render(requst, 'reciclaje/mispremios.html',{'premio_u':list})


def mi_perfil(request):
    return render(request, 'reciclaje/miperfil.html' )


## Editar propio usuario

@login_required
def perfil(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST,request.FILES ,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Tu información se ha actulizado')
            return redirect(to='homee')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'reciclaje/perfil.html', {'user_form': user_form})


class CambiarContraView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'reciclaje/cambiar_contra.html'
    success_message = 'Contraseña cambiada exitosamente'
    success_url = reverse_lazy('detallesUsuario')


##Entrega de dispocision final
class EntregaDispo(SuccessMessageMixin, CreateView):
    model = Entradas
    form_class = EntradasForm
    #form = Entradas
    #fields= [ "Curp", "DF", "Cantidad"]
    #success_message = 'Puntos agregados correctamente'
    
    def get_success_url(self):
        entradas =  Entradas.objects.all()
        userr = self.request.user.pk
        nombre = str(self.request.user.first_name)
        apellido = str(self.request.user.last_name)
        nombre_completo = nombre +" " +apellido
        ##try catch para validad que sea trabajador
        try:
            trabajador = Trabajador.objects.get(trbajador=userr)
        except:
            longitud = len(entradas)
            ent = entradas[longitud - 1]
            ent.delete()
            success_message = 'Ocurrio un error, este trabajador no esta registrado'
            messages.success (self.request, (success_message))    
            return reverse('DispoEngtrega')
        else:
            longitud = len(entradas)
            ent = entradas[longitud - 1]
            punto = ent.DF.puntoskg * ent.Cantidad 
            ent.puntos = punto
            ent.trabajador = nombre_completo
            ent.Curp.puntos = ent.Curp.puntos + punto
            ent.lugar = str(trabajador.lugar)
            ent.Curp.save()
            ent.save()
            success_message = 'Registro exitoso'
            messages.success (self.request, (success_message))    
            return reverse('detallesUsuario', args = [ent.Curp.pk])
         
    
    def post(self, request, *args, **kwarg):
        _mutaable = self.request.POST._mutable
        self.request.POST._mutable = True
        curp = self.request.POST['Curp']
        result = User.objects.get(CURP=curp)
        self.request.POST['Curp'] = result.pk
        return super().post(request, *args, **kwarg)
        
        
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

def search_user(request):
    query = request.GET.get("q",)
    results = User.objects.filter(CURP__icontains=query)
    data = {'results': list(results.values())}
    return JsonResponse(data)



     ##CRUD de Puntos de Reciclaje     

class PuntosReciclajelist(ListView):
    model = PuntosReciclaje
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.request.GET.get("buscar")
        if queryset:
            resultado = PuntosReciclaje.objects.filter(
                Q(nombre__icontains = queryset) 
            ).distinct()
            context['object_list'] = resultado
        return context

class PuntosReciclajeDetalle(DetailView):
    model = PuntosReciclaje

class PuntosReciclajeCreate(SuccessMessageMixin, CreateView):
    model = PuntosReciclaje
    form = PuntosReciclaje
    fields = "__all__"
    success_message = "Punto de reciclaje creado correctamente"
    
    def get_success_url(self):
        return reverse ('leerPuntosReciclaje')


class PuntosReciclajeActualizar(SuccessMessageMixin, UpdateView):
    model = PuntosReciclaje
    form = PuntosReciclaje
    fields = "__all__"
    success_message = "Punto de reciclaje actualizado correctamente"

    def get_success_url(self):
        return reverse ('leerPuntosReciclaje')

class PuntosReciclajeDelete(SuccessMessageMixin, DeleteView):
    model = PuntosReciclaje
    form = PuntosReciclaje
    fields = "__all__"

    def get_success_url(self):
        success_message = "Punto de reciclaje eliminado correctamente"
        messages.success (self.request, (success_message))
        return reverse ('leerPuntosReciclaje')


class TrabajadorActualizar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'reciclaje.admin'
    model = Trabajador
    form = Trabajador
    fields = ['lugar']
    success_message = "Trabajador registrado correctamente"

    def get_success_url(self):
        return reverse ('leerUsuarios')
    

class DescuentosActualizar(PermissionError, SuccessMessageMixin, UpdateView):
    permission_required = 'reciclaje.admin'
    model = Descuentos
    form = Descuentos
    fields = ['descuentos']
    success_message = "Descuento registrado correctamente"

    def get_success_url(self):
        return reverse ('leerUsuarios')
    


