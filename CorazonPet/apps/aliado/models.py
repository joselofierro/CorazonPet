from django.db import models


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % ('Aliados', instance.nombre, extension)


# Create your models here.
class Aliado(models.Model):
    nombre = models.CharField(max_length=30, blank=False, null=False)
    descuento = models.IntegerField()
    observacion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to=upload_location)

    def imagen_aliado(self):
        if self.logo:
            return '<img style="width:100px; height:100px;" src="%s">' % self.logo.url
        else:
            return 'No hay imagen'

    imagen_aliado.allow_tags = True
