from django.contrib import admin

# Register your models here.
from apps.sitio_mapa.models import SitioMapa


class SitioMapaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'imagen_admin', 'direccion', 'latitud', 'longitud', 'telefono', 'horario',
                    'tipo_sitio']


admin.site.register(SitioMapa, SitioMapaAdmin)
