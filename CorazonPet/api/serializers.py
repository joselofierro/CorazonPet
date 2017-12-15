from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from apps.aliado.models import Aliado
from apps.ciudad.models import Ciudad
from apps.historial_medicamento.models import HistorialMedicamento
from apps.historial_vacuna.models import HistorialVacuna
from apps.mascota_premium.models import MascotaPremium
from apps.media_mascota.models import ImagenesMascota
from apps.mascota.models import Mascota
from apps.mascota_calle.models import MascotaCalle
from apps.mascota_perdida.models import MascotaPerdida
from apps.medicamento.models import Medicamento
from apps.raza.models import Raza
from apps.recordatorio.models import Recordatorio, IdentificadorRecordatorio
from apps.sitio_mapa.models import SitioMapa
from apps.tipo_mascota.models import TipoMascota
from apps.tipo_sitio.models import TipoSitio
from apps.usuario.models import Usuario, VacunaUsuario
from apps.vacuna.models import Vacuna


class RazaSerializer(ModelSerializer):
    class Meta:
        model = Raza
        fields = ('id', 'nombre')


class TipoMascotaSerializer2(ModelSerializer):
    class Meta:
        model = TipoMascota
        fields = ('id', 'nombre')


class RazaMascotaSerializer(ModelSerializer):
    tipo_mascota = TipoMascotaSerializer2(many=False)

    class Meta:
        model = Raza
        fields = ('id', 'nombre', 'tipo_mascota')


class TipoMascotaSerializer(ModelSerializer):
    raza = RazaSerializer(many=True)

    class Meta:
        model = TipoMascota
        fields = ('id', 'nombre', 'raza')


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ('premium',)


class ListUserByParameter(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'nombre', 'apellido', 'telefono', 'email', 'premium')


class ImagenMascotasSerializer(ModelSerializer):
    # campo para pasar un metodo
    imagen = SerializerMethodField('get_foto_url')

    class Meta:
        model = ImagenesMascota
        fields = ('imagen',)

    def get_foto_url(self, obj):
        # obtenemos el contexto
        request = self.context.get('request')
        return request.build_absolute_uri(obj.imagen.url)


class MascotaSerializer(ModelSerializer):
    usuario = StringRelatedField(source='usuario.nombre')
    imagen = ImagenMascotasSerializer(many=True)
    raza = StringRelatedField(source='raza.nombre')

    class Meta:
        model = Mascota
        fields = '__all__'


class ReportarMascotaPremiumSerializer(ModelSerializer):
    class Meta:
        model = MascotaPerdida
        fields = ('id', 'direccion', 'celular', 'observacion', 'mascota')
        read_only_fields = ('id',)


class MascotaPerdidaSerializer(ModelSerializer):
    mascota = MascotaSerializer()

    class Meta:
        model = MascotaPerdida
        fields = ('id', 'direccion', 'celular', 'observacion', 'mascota')


class AliadoSerializer(ModelSerializer):
    class Meta:
        model = Aliado
        fields = '__all__'


class TipoSitioSerializer(ModelSerializer):
    class Meta:
        model = TipoSitio
        fields = ('nombre', 'marcador')


class SitioSerializer(ModelSerializer):
    tipo_sitio = TipoSitioSerializer()

    class Meta:
        model = SitioMapa
        fields = (
            'id', 'nombre', 'imagen', 'direccion', 'latitud', 'longitud', 'telefono', 'horario', 'tipo_sitio')


class CreateMascotaCalleSerializer(ModelSerializer):
    class Meta:
        model = MascotaCalle
        fields = ('latitud', 'longitud', 'direccion', 'observacion', 'telefono')


class MascotaCalleSerializer(ModelSerializer):
    class Meta:
        model = MascotaCalle
        fields = ('id', 'imagen', 'direccion', 'observacion')


class VacunaSerializer(ModelSerializer):
    class Meta:
        model = Vacuna
        fields = ('id', 'nombre',)


class CreateMascotaSerializer(ModelSerializer):
    class Meta:
        model = Mascota
        fields = (
            'dia', 'mes', 'nombre', 'sexo', 'raza', 'edad', 'usuario', 'aseguradora', 'numero_poliza',
            'numero_contacto', 'esterilizado'
        )


class MascotaUserSerializer(ModelSerializer):
    raza = RazaMascotaSerializer(many=False)
    usuario = StringRelatedField(source='usuario.nombre')
    imagen = ImagenMascotasSerializer(many=True)
    microchip = StringRelatedField(source='mascota_premium.microchip')
    # id de una mascota perdida en el modelo MascotaPerdida
    mascota_perdida = StringRelatedField(source='mascota_perdida.id')

    class Meta:
        model = Mascota
        fields = ('id', 'dia', 'mes', 'foto_perfil', 'raza', 'sexo', 'nombre', 'edad', 'usuario', 'imagen',
                  'esterilizado', 'microchip', 'aseguradora', 'numero_poliza', 'numero_contacto', 'mascota_perdida')


class AddVacunaHistorial(ModelSerializer):
    class Meta:
        model = HistorialVacuna
        fields = ('mascota', 'vacuna', 'prioridad', 'fecha_aplicacion', 'proxima_dosis', 'observacion')


class HistorialVacunaSerializer(ModelSerializer):
    vacuna = StringRelatedField(source='vacuna.nombre')

    class Meta:
        model = HistorialVacuna
        fields = ('vacuna', 'imagen', 'prioridad', 'fecha_aplicacion', 'proxima_dosis', 'observacion')


class GHistorialVacunaSerializer(ModelSerializer):
    class Meta:
        model = HistorialVacuna
        fields = ('vacuna', 'imagen', 'prioridad', 'fecha_aplicacion', 'proxima_dosis', 'observacion')


class MedicamentoSerializer(ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ('id', 'nombre',)


class AddHistorialMedicamento(ModelSerializer):
    class Meta:
        model = HistorialMedicamento
        fields = ('fecha', 'prioridad', 'mascota', 'medicamento', 'dosis', 'observacion')


class HistorialMedicamentoSerializer(ModelSerializer):
    medicamento = StringRelatedField(source='medicamento.nombre')

    class Meta:
        model = HistorialMedicamento
        fields = ('fecha', 'prioridad', 'medicamento', 'dosis', 'observacion')


class GHistorialMedicamentoSerializer(ModelSerializer):
    class Meta:
        model = HistorialMedicamento
        fields = ('fecha', 'prioridad', 'medicamento', 'dosis', 'observacion')


class CreateRecordatorioSerializer(ModelSerializer):
    class Meta:
        model = Recordatorio
        exclude = ('completado',)


class CreateIdentifierRecordatorioSerializer(ModelSerializer):
    class Meta:
        model = IdentificadorRecordatorio
        fields = '__all__'


class RecordatorioSerializer(ModelSerializer):
    class Meta:
        model = Recordatorio
        fields = '__all__'


class MediaMascotaSerializer(ModelSerializer):
    class Meta:
        model = ImagenesMascota
        fields = ('mascota',)


class MascotaPremiumSerializer(ModelSerializer):
    class Meta:
        model = MascotaPremium
        exclude = ('codigoqr',)


class CVacunaUsuarioSerializer(ModelSerializer):
    class Meta:
        model = VacunaUsuario
        fields = ('nombre', 'usuario')


class VacunaUsuarioSerializer(ModelSerializer):
    class Meta:
        model = VacunaUsuario
        fields = ('nombre',)


class GMascotaUserSerializer(ModelSerializer):
    class Meta:
        model = Mascota
        fields = ('sexo', 'nombre', 'raza', 'edad', 'dia', 'mes', 'aseguradora', 'numero_poliza', 'numero_contacto',
                  'esterilizado')


class CiudadSerializer(ModelSerializer):
    departamento = StringRelatedField(source='departamento.nombre')

    class Meta:
        model = Ciudad
        fields = ('nombre', 'departamento',)
