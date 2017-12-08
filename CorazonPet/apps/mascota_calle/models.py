from django.db import models


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % ('MascotaCalle', instance.fecha, extension)


# Create your models here.
class MascotaCalle(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to=upload_location)
    latitud = models.FloatField(max_length=40, blank=False, null=False)
    longitud = models.FloatField(max_length=40, blank=False, null=False)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    observacion = models.CharField(max_length=100)
    telefono = models.BigIntegerField()

    def imagen_mascota_calle(self):
        if self.imagen:
            return '<img style="width:100px;height:100px;" src="%s">' % self.imagen.url
        else:
            return 'No hay imagen'

    imagen_mascota_calle.allow_tags = True
