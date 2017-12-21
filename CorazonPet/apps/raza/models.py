from django.db import models

# Create your models here.
from apps.tipo_mascota.models import TipoMascota


class Raza(models.Model):
    nombre = models.CharField(max_length=150, blank=False, null=False)
    tipo_mascota = models.ForeignKey(TipoMascota, related_name='raza')

    def __str__(self):
        return self.nombre
