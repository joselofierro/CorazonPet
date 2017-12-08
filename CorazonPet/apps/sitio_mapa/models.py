from django.db import models

# Create your models here.
from apps.tipo_sitio.models import TipoSitio


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return "%s/%s.%s" % ('Sitio', instance.nombre, extension)


class SitioMapa(models.Model):
    imagen = models.ImageField(upload_to=upload_location, blank=False, null=False)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    latitud = models.FloatField(max_length=30, blank=False, null=False)
    longitud = models.FloatField(max_length=30, blank=False, null=False)
    telefono = models.BigIntegerField()
    horario = models.CharField(max_length=30, blank=False, null=False)
    tipo_sitio = models.ForeignKey(TipoSitio)

    def imagen_admin(self):
        if self.imagen:
            return '<img style="width:100px; height:100px;" src="%s">' % self.imagen.url
        else:
            return 'No hay imagen'

    imagen_admin.allow_tags = True
