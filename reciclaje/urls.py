from django.urls import path

from reciclaje.models import Premio_usuario
#Importar las vistas
from .views import *
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', home, name='homee'),
    path('catalogo/', RecompensasList.as_view(template_name = "reciclaje/catalogo.html"), name='catalogo'),

    path('usuarios/', UsuarioList.as_view(template_name = "reciclaje/UsuarioList.html"), name='leerUsuarios'),
    path('usuarios/detalle/<str:pk>', UsuarioDetalle.as_view(template_name="reciclaje/UsuarioDetail.html"), name='detallesUsuario'),
    path('usuarios/crear', UsuarioCreate.as_view(template_name = "reciclaje/UsuarioCreate.html"), name='crearUsuarios'),
    path('usuarios/editar/<str:pk>', UsuarioActulizar.as_view(template_name="reciclaje/UsuarioUpdate.html"), name='editarUsuario'),
    path('usuarios/eliminar/<str:pk>', UsuarioEliminar.as_view(template_name="reciclaje/UsuarioDelete.html"), name='eliminarUsuario'),

    path('premios/', permission_required('reciclaje.admin')(RecompensasList.as_view(template_name = "reciclaje/PremioList.html")), name='leerPremios'),
    path('premios/crear', RecompensasCreate.as_view(template_name = "reciclaje/PremioCreate.html"), name='crearPremios'),
    path('premios/detalle/<str:pk>', RecompensasDetalle.as_view(template_name="reciclaje/PremioDetail.html"), name='detallesPremio'),
    path('premios/editar/<str:pk>', RecompensasActulizar.as_view(template_name="reciclaje/PremioUpdate.html"), name='editarPremio'),
    path('premios/eliminar/<str:pk>', RecompensasEliminar.as_view(template_name="reciclaje/PremioDelete.html"), name='eliminarPremio'), 

    path('PuntosReciclaje/', PuntosReciclajelist.as_view(template_name = 'reciclaje/PuntosReciclajeList.html'), name = 'leerPuntosReciclaje'),
    path('PuntosReciclaje/detalle/<str:pk>', PuntosReciclajeDetalle.as_view(template_name = 'reciclaje/PuntosReciclajedetail.html'), name = 'detallePuntosReciclaje'),
    path('PuntosReciclaje/crear', PuntosReciclajeCreate.as_view(template_name = 'reciclaje/PuntosReciclajecreate.html'), name = 'crearPuntosReciclaje'),
    path('PuntosReciclaje/editar/<str:pk>', PuntosReciclajeActualizar.as_view(template_name = 'reciclaje/PuntosReciclajeUpdate.html'), name = 'editarPuntosReciclaje'),
    path('PuntosReciclaje/eliminar/<str:pk>', PuntosReciclajeDelete.as_view(template_name = 'reciclaje/PuntosReciclajeeliminar.html'), name = 'eliminarPuntosReciclaje'),




     path('dispofinal/', DispoFinallist.as_view(template_name = 'reciclaje/DispoFinalList.html'), name = 'leerDispoFinal'),
    path('dispofinal/detalle/<str:pk>', DispoFinalDetalle.as_view(template_name = 'reciclaje/dispofinaldetail.html'), name = 'detalleDispofinal'),
    path('dispofinal/crear', DispoFinalCreate.as_view(template_name = 'reciclaje/dispofinalcreate.html'), name = 'crearDispofinal'),
    path('dispofinal/editar/<str:pk>', DispoFinalActualizar.as_view(template_name = 'reciclaje/dispofinalUpdate.html'), name = 'editarDispofinal'),
    path('dispofinal/eliminar/<str:pk>', DispoFinalDelete.as_view(template_name = 'reciclaje/dispofinaleliminar.html'), name = 'eliminarDispofinal'),
    path('TablaEquivalencia/', Equivalencia.as_view(template_name = 'reciclaje/Equivalencia.html'), name = 'TablaEquivalencia'),
  
    

    path('premios/canjear', RecompensasUsuarioCreate.as_view(template_name = "reciclaje/PremioCanjear.html"), name='canjearPremios'),
    path('catalogo/buscar', buscar_productos, name='catalogo_b'),
    path('mis_premios/', ver_productos, name='misproductos'),
    path('mi_perfil/', mi_perfil, name='mi_perfil'),
    path('editar_perfil/', perfil, name='perfil'),
    path('cambio_contraseña/', CambiarContraView.as_view(), name='cambiar_contra'),
    path('dispocisionfinal/entrega', EntregaDispo.as_view(template_name = "reciclaje/DispocisionFinalEntrega.html"), name='DispoEngtrega'),

    
    path('trabajador/<str:pk>', TrabajadorActualizar.as_view(template_name = "reciclaje/trabajador.html"), name='trabajador'),
]