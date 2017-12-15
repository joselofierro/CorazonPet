from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from apps.usuario.models import *

"""def register_premium(modeladmin, request, queryset):
    permisos = Permission.objects.filter(user=request.user)
    print(permisos)
    up_premium = queryset.update(premium=True)
    for q in queryset:
        if up_premium == 1:
            message = "{} actualizado a premium".format(q.nombre)
        else:
            message = "%s usuarios actualizados a premium " % up_premium
        modeladmin.message_user(request, "%s" % message)


register_premium.short_descripcion = "Agregar a premium"""""


def register_premium(modeladmin, request, queryset):
    if request.user.has_perm('usuario.puede_agregar_premium'):
        print('tiene permiso')
    print('no tiene')


class UsuarioAdmin(admin.ModelAdmin):
    # solo podra modificar el User que tenga permisos para agregar premium
    list_display = ('id', 'nombre', 'apellido', 'edad', 'foto_perfil', 'verificado', 'telefono', 'email', 'premium')
    list_filter = ('nombre', 'email')
    search_fields = ['nombre']
    # prepopulated_fields = {"llave": ("valor",)}
    actions = [register_premium]

    """def get_actions(self, request):
        actions = super(UsuarioAdmin, self).get_action(request)
        if not request.user.has_perm('usuario.puede_agregar_premium'):
            del actions[register_premium]
        return actions"""


class VacunaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'usuario')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(VacunaUsuario, VacunaUsuarioAdmin)
