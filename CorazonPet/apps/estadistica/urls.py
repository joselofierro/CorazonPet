from django.conf.urls import url

from apps.estadistica.views import *

urlpatterns = [
    url(r'^mascotas_ciudad$', mascotas_ciudad, name="mascota_ciudad_estadistica"),
    url(r'^mascota_genero$', mascota_genero, name='mascota_genero_estadistica'),
    url(r'^tipos_mascota$', tipo_mascota, name='tipo_mascota_estadistica'),
    url(r'^razas_perros$', razas_mascota_perro, name='raza_mascota_estadistica'),
    url(r'^razas_gatos$', razas_mascota_gato, name='raza_mascota_estadistica2'),
    url(r'^mascotas_esterilizadas$', esterilizados, name='mascotas_esterilizadas_estadistica'),
    url(r'^mascotas_vacunas$', vacunados, name='mascotas_vacunas_estadistica'),
    url(r'^mascotas_poliza$', mascotas_poliza, name='mascotas_poliza_estadistica'),
    url(r'^mascotas_microchip$', mascotas_microchip, name='mascotas_premium_estadistica'),

]