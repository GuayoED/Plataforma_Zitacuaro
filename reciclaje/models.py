from email.policy import default
from enum import unique
from django.db import models
from django.forms import IntegerField
from django.contrib.auth.models import AbstractUser
from PIL import Image


class PuntosReciclaje(models.Model):
     nombre = models.CharField(primary_key=True, max_length = 40, default="")
     direccion = models.CharField( max_length = 40, default="")
     def __str__(self):     
        return self.nombre


class User(AbstractUser):

    Normal = 'Normal'
    ter_edad = 'Tercera Edad'
    Embarazadas = 'Embarazadas'

    Tipos =[
        (Normal, 'Normal'),
        (ter_edad, 'Tercera Edad'),
        (Embarazadas, 'Embarazadas')
    ]
    username = None
    CURP = models.CharField(unique=True,  max_length = 18)
    fechaNacimiento = models.DateField(null = True, blank = True)
    puntos = models.IntegerField(blank = True, null = True, default=0)
    pic = models.ImageField(default='unknown.jpg')
    tipo = models.CharField(choices=Tipos, default=Normal, max_length=12)
    #lugar = models.ForeignKey(PuntosReciclaje, on_delete=models.PROTECT, default='Sin lugar')
    

    USERNAME_FIELD = 'CURP'

    REQUIRED_FIELDS = []

    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.pic.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100,100)
    #         img.thumbnail(new_img)
    #         img.save(self.pic.path)

    class Meta:
        permissions = (("admin", "Funciones admin"),("recolector", "Funciones recolector"),("canjeador", "Funciones canjeador"))


class Premio(models.Model):
    nombre = models.CharField(max_length = 35)
    valor = models.DecimalField(default=1.0, max_digits=10, decimal_places=1)
    stock = models.IntegerField()
    imagen = models.ImageField()


    def __str__(self):
        return self.nombre


class Premio_usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    canjeado = models.BooleanField( default=False)

class DispoFinal(models.Model):
    #id = models.BigAutoField(primary_key=True, default= 1)
    nombre = models.CharField( max_length = 35)
    puntoskg = models.IntegerField(default=1)
    preciokg = models.DecimalField(default=1.0, max_digits=8, decimal_places=2)


    def __str__(self):
        return self.nombre




class Entradas(models.Model):
    #id = models.BigAutoField(primary_key=True, default= 0)
    trabajador = models.CharField( max_length = 40, default=" ")
    lugar = models.CharField( max_length = 40, default=" ")
    fecha = models.DateField(auto_now_add= True, null= True)
    Curp = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    DF = models.ForeignKey(DispoFinal, on_delete=models.CASCADE)
    Cantidad = models.FloatField(default = 0)
    puntos = models.FloatField(default=0)

    def __str__(self):
        return str(self.DF)

class Trabajador(models.Model):
    trbajador = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    lugar = models.ForeignKey(PuntosReciclaje, on_delete=models.CASCADE, default="")

class Descuentos(models.Model):
    nombre = models.CharField(max_length=40)
    descuentos = models.IntegerField()




