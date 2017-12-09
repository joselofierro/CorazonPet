from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token

from api.views import *

urlpatterns = [

    url(r'^tipo_mascotas', TipoMascotaAPI.as_view(), name='tipos_mascotas_api'),
    url(r'^usuarios$', User.as_view(), name='user_api'),
    url(r'^usuario/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', ListUserByCorreo.as_view(),name='user_id_api'),
    url(r'^login_user/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<contrasena>.*)$', login,name='login_user_api'),
    url(r'^mascotas_perdidas$', PetLostApi.as_view(), name='pet_lost_api'),
    url(r'^aliados', AliadoApi.as_view(), name='aliados_api'),
    url(r'^sitios', SitiosApi.as_view(), name='sitios_api'),
    url(r'^mascotas_perdida_calle', CreateMascotaCalleApi.as_view(), name='mascota_perdida_calle_api'),
    url(r'^mascotas_calle', MascotaCalleApi.as_view(), name='mascotas_calle_api'),
    url(r'^vacunas', VacunaApi.as_view(), name='vacuna_api'),
    url(r'^agregar_vacuna_historial', CreateHistorialVacuna.as_view(), name='add_historial_vacuna'),
    url(r'^historial_vacuna/(?P<pk>\d+)/$', ListHistorialVacunaApi.as_view(), name='historial_vacuna_api'),
    url(r'^medicamentos', MedicamentoApi.as_view(), name='medicamento_api'),
    url(r'^agregar_medicamento_historial', CreateHistorialMedicamento.as_view(), name='add_historial_medicamento'),
    url(r'^historial_medicamento/(?P<pk>\d+)/$', ListHistorialMedicamentoApi.as_view(), name='historial_medico_api'),
    url(r'^agregar_recordatorio', CreateRecordatorio.as_view(), name='agregar_recordatorio_api'),
    url(r'^asignar_identificador_recordatorio', CreateIdentifierRecordatorio.as_view(), name='agregar_recordatorio_api'),
    url(r'^recordatorios/(?P<pk>\d+)/$', ListRecordatorioApi.as_view(), name='historial_medico_api'),
    url(r'^crear_mascota', CreateMascotaApi.as_view(), name='mascota_api'),
    url(r'^token-auth', obtain_jwt_token),
    url(r'^mascotas_user/(?P<pk>\d+)/$', MascotaUserApi.as_view(), name='mascota_user_api'),
    url(r'^agregar_foto_mascota', CreateMascotaMedia.as_view(), name='mascota_media_api'),
    url(r'^imagenes_mascota/(?P<id_mascota>\d+)/$', ListMediaMascota.as_view(), name='imagenes_mascota_api'),
    url(r'^cambiar_estado_recordatorio', status_recordatorio, name='cambiar_estado_recordatorio'),
    url(r'^agregar_mascota_premium', MascotaPremiumAPI.as_view(), name='mascota_premium_api'),
    url(r'^create_fcm', CreateFCM.as_view(), name='create_fcm_api'),
    url(r'^encontre_mascota_premium', find_pet_premium, name='encontre_mascota_premium')
]

# urlpatterns = format_suffix_patterns(urlpatterns)
