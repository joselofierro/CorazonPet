from django.db import models


# Create your models here.
def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return "%s/%s.%s" % ('Marcador_Sitio', instance.nombre, extension)


class TipoSitio(models.Model):
    nombre = models.CharField(max_length=20, blank=False, null=False)
    marcador = models.ImageField(blank=False, null=False, upload_to=upload_location)

    def __str__(self):
        return self.nombre

    def imagen_sitio(self):
        if self.marcador:
            return '<img style="width:43px;height:50px;" src="%s">' % self.marcador.url
        else:
            return 'No hay imagen'

    imagen_sitio.allow_tags = True

