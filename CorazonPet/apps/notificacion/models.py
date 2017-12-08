from django.db import models


# Create your models here.
class Notificacion(models.Model):
    fecha = models.TimeField(auto_now_add=True)
    hora = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=20, blank=False, null=False, default='CorazónPet')
    mensaje = models.CharField(max_length=100, null=False, blank=False)


