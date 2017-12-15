from django.contrib import admin

# Register your models here.
from apps.ciudad.models import Ciudad


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')


admin.site.register(Ciudad, CiudadAdmin)
