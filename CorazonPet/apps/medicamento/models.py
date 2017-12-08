from django.db import models


# Create your models here.
class Medicamento(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre
