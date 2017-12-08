from django.contrib import admin

# Register your models here.
from apps.tipo_sitio.models import TipoSitio


class TipoSitioAdmin(admin.ModelAdmin):
    search_fields = ['nombre', ]
    list_display = ['nombre', 'imagen_sitio']


admin.site.register(TipoSitio, TipoSitioAdmin)
