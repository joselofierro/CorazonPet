from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % ('HistorialMedicamento', instance.medicamento, extension)


class HistorialMedicamento(models.Model):
    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'

    Prioridad = (
        (BAJA, 'Baja'),
        (MEDIA, 'Media'),
        (ALTA, 'Alta')
    )

    fecha = models.DateField(null=True, blank=True)
    prioridad = models.CharField(max_length=10, blank=False, null=False, choices=Prioridad)
    mascota = models.ForeignKey(Mascota)
    medicamento = models.CharField(max_length=100, blank=False, null=False)
    imagen = models.ImageField(upload_to=upload_location)
    dosis = models.CharField(max_length=15, blank=False, null=False)
    observacion = models.CharField(max_length=200, blank=True, null=False)

    def image_medicamento(self):
        if self.imagen:
            return '<img style="width:200px; height:200px;" src="%s">' % self.imagen.url
        else:
            return 'No hay imagen'

    image_medicamento.allow_tags = True
