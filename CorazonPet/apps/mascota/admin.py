from django.contrib import admin

# Register your models here.
from apps.mascota.models import Mascota


class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'admin_image', 'sexo', 'raza', 'edad', 'usuario')
    list_filter = ('raza', 'usuario')
    search_fields = ('nombre',)
    list_per_page = 10


admin.site.register(Mascota, MascotaAdmin)
