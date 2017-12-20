from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


class Recordatorio(models.Model):
    ASEO = 'Aseo'
    MEDICO = 'Medico'
    ALIMENTO = 'Alimento'
    OTRO = 'Otro'

    Categoria = (
        (ASEO, 'Aseo'),
        (MEDICO, 'Medico'),
        (ALIMENTO, 'Alimento'),
        (OTRO, 'Otro')
    )

    mascota = models.ForeignKey(Mascota)
    categoria = models.CharField(blank=False, null=False, choices=Categoria, max_length=10)
    actividad = models.CharField(max_length=50)
    fecha = models.DateField(auto_now_add=True, blank=True)
    hora = models.TimeField(null=False, blank=False, default="08:00")
    lunes = models.NullBooleanField(null=False, default=False)
    martes = models.NullBooleanField(null=False, default=False)
    miercoles = models.NullBooleanField(null=False, default=False)
    jueves = models.NullBooleanField(null=False, default=False)
    viernes = models.NullBooleanField(null=False, default=False)
    sabado = models.NullBooleanField(null=False, default=False)
    domingo = models.NullBooleanField(null=False, default=False)
    observacion = models.TextField(null=True, blank=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return self.actividad


class IdentificadorRecordatorio(models.Model):
    recordatorio = models.ForeignKey(Recordatorio, related_name='recordatorio_identificador')
    identificador = models.IntegerField(blank=False, null=False, default=1)

    def __str__(self):
        return '{}_{}'.format(self.recordatorio.actividad, self.identificador)
