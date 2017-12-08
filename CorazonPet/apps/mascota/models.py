from django.db import models

# Create your models here.
from apps.raza.models import Raza
from apps.tipo_mascota.models import TipoMascota
from apps.usuario.models import Usuario


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return "%s/%s.%s" % ('Mascota', instance.nombre, extension)


class Mascota(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'

    Genero = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    )

    dia = models.IntegerField(blank=False, null=False)
    mes = models.IntegerField(blank=False, null=False)
    foto_perfil = models.ImageField(upload_to=upload_location)
    nombre = models.CharField(max_length=30, blank=False, null=False)
    sexo = models.CharField(max_length=10, blank=False, null=False, choices=Genero)
    raza = models.ForeignKey(Raza)
    edad = models.FloatField(blank=False, null=False)
    usuario = models.ForeignKey(Usuario)
    aseguradora = models.TextField(max_length=50, blank=True)
    numero_poliza = models.TextField(max_length=50, blank=True)
    numero_contacto = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return '{} de {} {}'.format(self.nombre, self.usuario.nombre, self.usuario.apellido)

    def admin_image(self):
        if self.foto_perfil:
            return '<img style="width:100px; height:100px;" src="%s">' % self.foto_perfil.url
        else:
            return 'No hay imagen'

    # traduzca de etiqueta html a imagen
    admin_image.allow_tags = True
