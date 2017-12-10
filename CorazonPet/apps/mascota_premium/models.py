import qrcode as qrcode
from django.core.files import File
from django.db import models

# Create your models here.
from apps.mascota.models import Mascota


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return "%s/%s.%s" % ('Codigoqrmascota', instance.mascota.nombre, extension)


class MascotaPremium(models.Model):
    mascota = models.OneToOneField(Mascota)
    microchip = models.TextField(max_length=15)
    codigoqr = models.ImageField(upload_to=upload_location, blank=True)

    def __str__(self):
        return self.mascota.nombre

    """# metodo que guarda la instancia del modelo al crearlo
    def save(self):
        self.generate_qr()
        super(MascotaPremium, self).save()

    def generate_qr(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(self.microchip)
        # compila la data a un array de QR
        qr.make(fit=True)

        filename = 'qrcode_%s_%s.png' % (self.mascota.nombre, self.microchip)

        # creamos la imagen QR
        img = qr.make_image()

        from django.conf import settings
        img.save(settings.MEDIA_ROOT + "Codigoqrmascota/" + filename)

        with open(settings.MEDIA_ROOT + "Codigoqrmascota/" + filename, "rb") as reopen:
            django_file = File(reopen)
            self.codigoqr.save(filename, django_file, save=False)"""

    def imagen_qr(self):
        if self.codigoqr:
            return "<img style='width:100px; height:100px;' src='%s'>" % self.codigoqr.url
        else:
            return 'No hay QR'

    imagen_qr.allow_tags = True
