from django.contrib import admin

# Register your models here.
from apps.media_mascota.models import ImagenesMascota


class ImagenMascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'admin_image')
    list_filter = ('mascota',)


admin.site.register(ImagenesMascota, ImagenMascotaAdmin)
