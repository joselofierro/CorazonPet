from django.db import models

# Create your models here.
from apps.mascota.models import Mascota
from apps.usuario.models import VacunaUsuario
from apps.vacuna.models import Vacuna


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % ('HistorialVacuna', instance.mascota.nombre, extension)


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
    vacuna = models.ManyToManyField(Vacuna, blank=True)
    prioridad = models.CharField(max_length=10, blank=False, null=False, choices=Prioridad)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField()
    observacion = models.CharField(max_length=200, blank=True, null=False, default="")
    vacuna_usuario = models.ManyToManyField(VacunaUsuario, blank=True)
