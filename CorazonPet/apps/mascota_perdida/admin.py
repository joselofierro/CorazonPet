from django.contrib import admin

# Register your models here.
from apps.mascota_perdida.models import MascotaPerdida


class MascotaPerdidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'volante_pet', 'mascota', 'direccion', 'celular', 'observacion')
    list_per_page = 10
    list_filter = ('mascota',)


admin.site.register(MascotaPerdida, MascotaPerdidaAdmin)
