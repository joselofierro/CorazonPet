from django.contrib import admin

# Register your models here.
from apps.aliado.models import Aliado


class AliadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descuento', 'observacion', 'imagen_aliado', 'sitio')
    search_fields = ('nombre',)


admin.site.register(Aliado, AliadoAdmin)
