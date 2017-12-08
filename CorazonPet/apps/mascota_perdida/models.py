from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


class MascotaPerdida(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    mascota = models.OneToOneField(Mascota)
    latitud = models.FloatField(max_length=40, blank=False, null=False)
    longitud = models.FloatField(max_length=40, blank=False, null=False)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    celular = models.BigIntegerField(blank=False, null=False)
    observacion = models.CharField(max_length=200, blank=True, null=True)
