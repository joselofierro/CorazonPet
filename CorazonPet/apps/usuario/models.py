from django.db import models

# Create your models here.
import uuid

from django.db import models


# Create your models here.
class Usuario(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'

    Genero = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )

    idFacebook = models.CharField(blank=True, null=True, max_length=150)
    nombre = models.CharField(max_length=30, blank=False, null=False)
    apellido = models.CharField(max_length=30, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    genero = models.CharField(blank=True, null=True, max_length=2, choices=Genero)
    foto = models.TextField(blank=True, null=True)
    verificado = models.BooleanField(default=True)
    telefono = models.BigIntegerField(blank=True, default=0, null=False)
    email = models.CharField(max_length=30, blank=False, null=False, unique=True)
    premium = models.BooleanField(default=False)
    contrasena = models.CharField(blank=True, null=False, default="", max_length=100)

    class Meta:
        permissions = (
            ('puede_agregar_premium', 'Puede agregar a premium'),
        )

    def foto_perfil(self):
        if self.foto:
            return '<img style="width:100px;height:100px;" src="%s">' % self.foto
        else:
            return 'No hay imagen'

    foto_perfil.allow_tags = True

    def __str__(self):
        return self.nombre
