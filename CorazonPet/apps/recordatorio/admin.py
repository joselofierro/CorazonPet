from django.contrib import admin


# Register your models here.
from apps.recordatorio.models import Recordatorio, IdentificadorRecordatorio


class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'mascota', 'categoria', 'actividad', 'hora', 'completado', 'observacion')
    list_filter = ('categoria', 'mascota')
    search_fields = ['actividad']
    # prepopulated_fields = {"llave": ("valor",)}


admin.site.register(Recordatorio, RecordatorioAdmin)
admin.site.register(IdentificadorRecordatorio)
