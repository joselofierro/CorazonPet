from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return "%s/%s.%s" % ('MascotaPerdida', instance.mascota.nombre, extension)


class MascotaPerdida(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    mascota = models.OneToOneField(Mascota, related_name='mascota_perdida')
    volante = models.ImageField(blank=True, null=True, upload_to=upload_location)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    celular = models.BigIntegerField(blank=False, null=False)
    observacion = models.CharField(max_length=200, blank=True, null=True)

    def volante_pet(self):
        if self.volante:
            return '<img style="width:100px;height:100px;" src="%s">' % self.volante.url
        else:
            return 'No hay imagen'

    volante_pet.allow_tags =True
