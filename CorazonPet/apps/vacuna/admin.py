from django.contrib import admin

# Register your models here.
from apps.vacuna.models import Vacuna


class VacunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


admin.site.register(Vacuna, VacunaAdmin)
