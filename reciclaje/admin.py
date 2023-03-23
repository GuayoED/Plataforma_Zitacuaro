from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User)
admin.site.register(Premio)
admin.site.register(Premio_usuario)
admin.site.register(DispoFinal)
admin.site.register(Entradas)
admin.site.register(PuntosReciclaje)
admin.site.register(Trabajador)
admin.site.register(Descuentos)




