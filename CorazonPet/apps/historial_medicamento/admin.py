from django.contrib import admin

# Register your models here.
from apps.historial_medicamento.models import HistorialMedicamento


class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'mascota', 'medicamento', 'image_medicamento', 'prioridad', 'dosis', 'observacion')
    list_filter = ('mascota', 'medicamento')


admin.site.register(HistorialMedicamento, HistorialMedicoAdmin)
