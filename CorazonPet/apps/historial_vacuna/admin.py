from django.contrib import admin

# Register your models here.
from apps.historial_vacuna.models import HistorialVacuna


class HistorialVacunaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'vacuna', 'image_vacuna', 'prioridad', 'fecha_aplicacion', 'proxima_dosis', 'observacion')
    list_filter = ('vacuna',)
    search_fields = ('vacuna', 'mascota')
    list_per_page = 10


admin.site.register(HistorialVacuna, HistorialVacunaAdmin)
