from django.contrib import admin

# Register your models here.
from fcm_django.models import FCMDevice

from apps.notificacion.models import Notificacion


class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'titulo', 'mensaje')

    # momento a guardar la instancia de la notificacion
    def save_model(self, request, obj, form, change):
        titulo = obj.titulo
        mensaje = obj.mensaje

        # Obtenemos los usuarios Android
        usuarios_android = FCMDevice.objects.filter(type='android')

        # Enviamos la notificacion
        usuarios_android.send_message(data={'titulo': titulo, 'mensaje': mensaje})

        # Obtenemos los usuarios ios
        usuarios_ios = FCMDevice.objects.filter(type='ios')
        # Enviamos la notificacion
        usuarios_ios.send_message(title=titulo, body=mensaje, sound='default')
        super(NotificacionAdmin, self).save_model(request, obj, form, change)


admin.site.register(Notificacion, NotificacionAdmin)
