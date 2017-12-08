from django.db import models


# Create your models here.


class TipoMascota(models.Model):
    nombre = models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return self.nombre
