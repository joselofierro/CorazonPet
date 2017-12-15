from django.db import models

# Create your models here.
from apps.departamento.models import Departamento


class Ciudad(models.Model):
    nombre = models.CharField(max_length=70, blank=False, null=False)
    departamento = models.ForeignKey(Departamento)

    def __str__(self):
        return self.nombre
