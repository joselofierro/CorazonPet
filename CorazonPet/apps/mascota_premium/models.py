from io import BytesIO

import qrcode as qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return "%s/%s.%s" % ('Codigoqrmascota', instance.mascota.nombre, extension)


class MascotaPremium(models.Model):
    mascota = models.OneToOneField(Mascota, related_name='mascota_premium')
    microchip = models.TextField(max_length=15)
    codigoqr = models.ImageField(upload_to=upload_location, blank=True)

    def __str__(self):
        return self.mascota.nombre

    # metodo que guarda la instancia del modelo al crearlo
    def save(self, **kwargs):
        self.generate_qr()
        super(MascotaPremium, self).save(**kwargs)

    def generate_qr(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(self.microchip)
        # compila la data a un array de QR
        qr.make(fit=True)
        # creamos la imagen QR
        img = qr.make_image()

        buffer = BytesIO()
        # guardamos el buffer en la imagen
        img.save(buffer)
        filename = 'qrcode_%s.png' % self.mascota.nombre
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.getbuffer, None)
        # guardamos la imagen QR en el campo de la imagen
        self.codigoqr.save(filename, filebuffer, False)

    def imagen_qr(self):
        if self.codigoqr:
            return "<img style='width:100px; height:100px;' src='%s'>" % self.codigoqr.url
        else:
            return 'No hay QR'

    imagen_qr.allow_tags = True
