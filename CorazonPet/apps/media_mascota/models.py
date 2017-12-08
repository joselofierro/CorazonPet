from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % ('ImagenesMascota', instance.mascota.nombre, extension)


class ImagenesMascota(models.Model):
    mascota = models.ForeignKey(Mascota, related_name='imagen')
    imagen = models.ImageField(upload_to=upload_location)
    fecha = models.DateField(auto_now_add=True, blank=True)
    hora = models.TimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-fecha', '-hora']

    def admin_image(self):
        if self.imagen:
            return '<img style="width:100px; height:100px;" src="%s">' % self.imagen.url
        else:
            return 'No hay imagen'

    admin_image.allow_tags = True
