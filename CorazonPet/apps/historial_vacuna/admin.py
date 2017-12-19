from django.contrib import admin

# Register your models here.
from apps.historial_vacuna.models import HistorialVacuna


class HistorialVacunaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'mascota', 'vacunas', 'prioridad', 'fecha_aplicacion', 'proxima_dosis', 'observacion')
    list_filter = ('vacuna',)
    search_fields = ('vacuna', 'mascota')
    list_per_page = 10

    def vacunas(self, obj):
        vacunas = ""
        vacunas_usuario = ""
        for vacuna in obj.vacuna.all():
            vacunas += vacuna.nombre + ", "

        for vacuna_usuario in obj.vacuna_usuario.all():
            vacunas_usuario += vacuna_usuario.nombre + ", "
        return "{} {}".format(vacunas, vacunas_usuario)


admin.site.register(HistorialVacuna, HistorialVacunaAdmin)
