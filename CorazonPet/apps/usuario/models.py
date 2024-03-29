from django.contrib.auth.models import User
from django.db import models

# Create your models here.
import uuid

from django.db import models

# Create your models here.
from apps.ciudad.models import Ciudad
from apps.departamento.models import Departamento


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
    telefono = models.BigIntegerField(blank=True, default=0, null=False)
    email = models.CharField(max_length=30, blank=False, null=False, unique=True)
    premium = models.BooleanField(default=False)
    contrasena = models.CharField(blank=True, null=False, default="", max_length=100)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True)
    user_token = models.OneToOneField(User, null=True, blank=True)

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


class VacunaUsuario(models.Model):
    nombre = models.CharField(max_length=70, blank=False, null=False)
    usuario = models.ForeignKey(Usuario)

    def __str__(self):
        return self.nombre


class RecuperarContrasena(models.Model):
    usuario = models.OneToOneField(Usuario)
    token = models.TextField(blank=False, null=False)
