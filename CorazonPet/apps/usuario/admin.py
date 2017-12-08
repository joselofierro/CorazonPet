from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from apps.usuario.models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    # solo podra modificar el User que tenga permisos para agregar premium
    list_display = ('id', 'nombre', 'apellido', 'edad', 'foto_perfil', 'verificado', 'telefono', 'email', 'premium')
    list_filter = ('nombre', 'email')
    search_fields = ['nombre']
    # prepopulated_fields = {"llave": ("valor",)}
    actions = ['register_premium']

    def register_premium(self, request, queryset):
        permisos = Permission.objects.filter(user=request.user)
        print(queryset)
        if permisos:
            print(permisos)
            up_premium = queryset.update(premium=True)
            usuario = Usuario.objects.get(id=queryset)
            if up_premium == 1:
                message = "{} actualizado a premium".format(usuario.nombre)
            else:
                message = "%s usuarios actualizados a premium " % up_premium
            self.message_user(request, "%s" % message)
        else:
            print('Error')

    register_premium.short_descripcion = "Agregar a premium"


admin.site.register(Usuario, UsuarioAdmin)
