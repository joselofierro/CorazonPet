from django.db import models

# Create your models here.
from apps.mascota.models import Mascota
from apps.vacuna.models import Vacuna


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % ('HistorialVacuna', instance.vacuna, extension)


class HistorialVacuna(models.Model):
    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'

    Prioridad = (
        (BAJA, 'Baja'),
        (MEDIA, 'Media'),
        (ALTA, 'Alta')
    )
    mascota = models.ForeignKey(Mascota)
    vacuna = models.ForeignKey(Vacuna)
    imagen = models.ImageField(upload_to=upload_location)
    prioridad = models.CharField(max_length=10, blank=False, null=False, choices=Prioridad)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField()
    observacion = models.CharField(max_length=200, blank=True, null=False, default="")

    def image_vacuna(self):
        if self.imagen:
            return '<img style="width:200px; height:200px;" src="%s">' % self.imagen.url
        else:
            return 'No hay imagen'

    image_vacuna.allow_tags = True
