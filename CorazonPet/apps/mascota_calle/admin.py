from django.contrib import admin

# Register your models here.
from apps.mascota_calle.models import MascotaCalle


class MascotaCalleAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'imagen_mascota_calle', 'latitud', 'longitud', 'direccion', 'telefono')
    list_per_page = 10


admin.site.register(MascotaCalle, MascotaCalleAdmin)
