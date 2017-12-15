from django.contrib import admin

# Register your models here.
from apps.mascota_premium.models import MascotaPremium


class MascotaPremiumAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'microchip', 'imagen_qr')
    search_fields = ('mascota',)
    exclude = ('codigoqr', )


admin.site.register(MascotaPremium, MascotaPremiumAdmin)
