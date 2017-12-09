import base64
from fcm_django.api.rest_framework import FCMDeviceSerializer
from fcm_django.models import FCMDevice
from rest_framework import request
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.views import *
from api.serializers import *
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import check_password, make_password


# API con el listado de tipos de mascota y su respectiva razas
class TipoMascotaAPI(ListAPIView):
    serializer_class = TipoMascotaSerializer

    def get_queryset(self):
        return TipoMascota.objects.all().order_by('nombre')


# API PARA CREAR USUARIO
class User(CreateAPIView):
    serializer_class = CreateUserSerializer

    def get_queryset(self):
        return Usuario.objects.all()

    def post(self, request):
        usuario_serializer = CreateUserSerializer(data=request.data)
        if usuario_serializer.is_valid():
            contrasena = request.data['contrasena']
            contrasena_cifrada = make_password(contrasena, salt=None, hasher='sha1')
            if contrasena != "":
                usuario_obj = usuario_serializer.save()
                usuario_obj.contrasena = contrasena_cifrada
                usuario_obj.save()
                return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)
            return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login(request, email, contrasena):
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(email=email, contrasena=contrasena)
            serializer = CreateUserSerializer(usuario, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'data': 'Credenciales incorrectas'}, status=status.HTTP_404_NOT_FOUND)


# API de listado de usuario por correo
class ListUserByCorreo(APIView):
    def get(self, request, email):
        try:
            user_obj = Usuario.objects.get(email=email)
            user_serializer = ListUserByParameter(user_obj)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'data': 'No existe usuario con ese correo'}, status=status.HTTP_404_NOT_FOUND)


# API PARA REPORTAR MASCOTAS PERDIDAS Y LISTAR MASCOTAS PERDIDAS
class PetLostApi(APIView):
    def post(self, request):
        mascota_serializer = ReportarMascotaPremiumSerializer(data=request.data)
        if mascota_serializer.is_valid():
            mascota_serializer.save()
            return Response(mascota_serializer.data, status=status.HTTP_201_CREATED)
        return Response(mascota_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        mascota_perdida_obj = MascotaPerdida.objects.all().order_by('-fecha', '-hora')
        mascota_perdida_serializer = MascotaPerdidaSerializer(mascota_perdida_obj, many=True,
                                                              context={'request': request})
        return Response(mascota_perdida_serializer.data, status=status.HTTP_200_OK)


# Listado de aliados
class AliadoApi(ListAPIView):
    serializer_class = AliadoSerializer

    def get_queryset(self):
        return Aliado.objects.all().order_by('nombre', 'descuento')


# listado de sitios
class SitiosApi(ListAPIView):
    serializer_class = SitioSerializer

    def get_queryset(self):
        return SitioMapa.objects.all().order_by('nombre')


# API PARA REPORTAR MASCOTA PERDIDA
class CreateMascotaCalleApi(CreateAPIView):
    serializer_class = CreateMascotaCalleSerializer

    def post(self, request, *args, **kwargs):
        mascota_calle = CreateMascotaCalleSerializer(data=request.data)
        if mascota_calle.is_valid():
            img_64 = request.data['imagen']
            img_deco = base64.b64decode(img_64)
            obj_media = mascota_calle.save()
            obj_media.imagen = ContentFile(img_deco, name='imagen_mascota_calle' + '.jpg')
            obj_media.save()

            return Response({'data': 'Mascota reportada con exito'}, status=status.HTTP_201_CREATED)

        return Response({'error': mascota_calle.errors}, status=status.HTTP_400_BAD_REQUEST)


# API DE MASCOTAS PERDIDAS NO REGISTRADAS
class MascotaCalleApi(ListAPIView):
    serializer_class = MascotaCalleSerializer

    def get_queryset(self):
        return MascotaCalle.objects.all().order_by('-fecha', '-hora')


# API PARA LISTAR VACUNAS
class VacunaApi(ListAPIView):
    """def post(self, request):
        if Vacuna.objects.filter(nombre=request.data['nombre']).exists():
            return Response({'data': 'Vacuna ya existe'}, status=status.HTTP_200_OK)
        else:
            vacuna_serializer = VacunaSerializer(data=request.data)
            if vacuna_serializer.is_valid():
                vacuna_serializer.save()
                return Response({'vacuna': vacuna_serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'error': vacuna_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)"""

    serializer_class = VacunaSerializer

    def get_queryset(self):
        return Vacuna.objects.all().order_by('nombre')


# API PARA CREAR VACUNA A LA MASCOTA EN HISTORIAL VACUNA
class CreateHistorialVacuna(CreateAPIView):
    serializer_class = AddVacunaHistorial

    def post(self, request, *args, **kwargs):
        historial_vacuna_serializer = AddVacunaHistorial(data=request.data)
        if historial_vacuna_serializer.is_valid():
            img_64 = request.data['imagen']
            img_deco = base64.b64decode(img_64)

            obj_history_vacuna = historial_vacuna_serializer.save()
            obj_history_vacuna.imagen = ContentFile(img_deco,
                                                    name='vacuna_' + obj_history_vacuna.mascota.nombre + "_" + str(
                                                        obj_history_vacuna.mascota.id) + "_" + obj_history_vacuna.vacuna.nombre + '.jpg')
            obj_history_vacuna.save()

            return Response({'data': 'Vacuna creada'}, status=status.HTTP_201_CREATED)
        return Response({'error': historial_vacuna_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Listado de historias de vacunas por el id de la mascota
class ListHistorialVacunaApi(ListAPIView):
    serializer_class = HistorialVacunaSerializer

    def get_queryset(self):
        return HistorialVacuna.objects.filter(mascota__id=self.kwargs['pk'])


# API PARA LISTAR MEDICAMENTOS
class MedicamentoApi(ListAPIView):
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        return Medicamento.objects.all().order_by('nombre')


# API PARA CREAR MEDICAMENTO A LA MASCOTA EN EL HISTORIAL MEDICO
class CreateHistorialMedicamento(CreateAPIView):
    serializer_class = AddHistorialMedicamento

    def post(self, request, *args, **kwargs):
        historial_medicamento = AddHistorialMedicamento(data=request.data)
        if historial_medicamento.is_valid():
            img_64 = request.data['imagen']
            img_deco = base64.b64decode(img_64)

            obj_historial_medicamento = historial_medicamento.save()

            obj_historial_medicamento.imagen = ContentFile(img_deco,
                                                           name='medicamento_' + obj_historial_medicamento.mascota.nombre + "_" + str(
                                                               obj_historial_medicamento.mascota.id) + "_" + obj_historial_medicamento.medicamento.nombre + '.jpg')
            obj_historial_medicamento.save()
            return Response({'data': 'Medicamento creado'}, status=status.HTTP_201_CREATED)
        return Response({'error': historial_medicamento.errors}, status=status.HTTP_400_BAD_REQUEST)


# HISTORIAL MEDICO POR EL ID DE LA MASCOTA
class ListHistorialMedicamentoApi(ListAPIView):
    serializer_class = HistorialMedicamentoSerializer

    def get_queryset(self):
        return HistorialMedicamento.objects.filter(mascota__id=self.kwargs['pk'])


# API PARA CREAR RECORDATORIO
class CreateRecordatorio(CreateAPIView):
    serializer_class = CreateRecordatorioSerializer


# API PARA RELACIONAR LOS IDENTIFICADORES DE LOS RECORDATORIOS
class CreateIdentifierRecordatorio(CreateAPIView):
    serializer_class = CreateIdentifierRecordatorioSerializer


# listado de recordatorio por el id de la mascota
class ListRecordatorioApi(ListAPIView):
    serializer_class = RecordatorioSerializer

    def get_queryset(self):
        return Recordatorio.objects.filter(mascota__id=self.kwargs['pk'])


# API PARA CREAR MASCOTAS
class CreateMascotaApi(CreateAPIView):
    serializer_class = CreateMascotaSerializer

    def post(self, request, *args, **kwargs):
        # recibimos el json
        mascota_serializer = CreateMascotaSerializer(data=request.data)
        # si es valido el serializer
        if mascota_serializer.is_valid():
            # recibimos la imagen
            img_64 = request.data['foto_perfil']
            # la descodificamos
            img_deco = base64.b64decode(img_64)
            print(img_deco)
            # instancia del serializer
            instancia_mascota = mascota_serializer.save()
            # pasamos la imagen decodificada a un archivo (png, jpg)
            instancia_mascota.foto_perfil = ContentFile(img_deco, name='mascota_' + str(instancia_mascota.id) + '.jpg')
            instancia_mascota.save()
            return Response({'data': 'Mascota creada'}, status=status.HTTP_200_OK)

        return Response({'error': mascota_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# API QUE RETORNA LAS MASCOTAS ASOCIADAS AL USUARIO
class MascotaUserApi(ListAPIView):
    serializer_class = MascotaUserSerializer

    def get_queryset(self):
        return Mascota.objects.filter(usuario__id=self.kwargs['pk'])


# API PARA AGREGAR FOTOS A LA MASCOTA
class CreateMascotaMedia(CreateAPIView):
    serializer_class = MediaMascotaSerializer

    def post(self, request, *args, **kwargs):
        media_mascota = MediaMascotaSerializer(data=request.data)
        if media_mascota.is_valid():
            img_64 = request.data['imagen']
            img_deco = base64.b64decode(img_64)
            obj_media = media_mascota.save()
            obj_media.imagen = ContentFile(img_deco, name='imagen_mascota_' + obj_media.mascota.nombre + "_" + str(
                obj_media.mascota.id) + '.jpg')
            obj_media.save()

            return Response({'data': 'Imagen Creada'}, status=status.HTTP_201_CREATED)

        return Response({'error': media_mascota.errors}, status=status.HTTP_400_BAD_REQUEST)


# API PARA OBTENER LAS FOTOS DE UNA MASCOTA
class ListMediaMascota(ListAPIView):
    serializer_class = ImagenMascotasSerializer

    def get_queryset(self):
        return ImagenesMascota.objects.filter(mascota__id=self.kwargs['id_mascota']).order_by('-fecha', '-hora')


# API PARA CAMBIAR ESTADO DEL RECORDATORIO
@api_view(['put'])
def status_recordatorio(request):
    try:
        recordatorio = request.data['recordatorio']

        estado = request.data['estado']

        recordatorio_obj = Recordatorio.objects.get(id=recordatorio)

        recordatorio_obj.completado = estado

        recordatorio_obj.save()

        return Response({'data': 'Actualizado'}, status=status.HTTP_200_OK)

    except Recordatorio.DoesNotExist:
        return Response({'data': 'Recordatorio no existe'}, status=status.HTTP_400_BAD_REQUEST)


# API PARA GENERAR MASCOTA PREMIUM
class MascotaPremiumAPI(CreateAPIView):
    serializer_class = MascotaPremiumSerializer


# Api para crear las notificaciones
class CreateFCM(CreateAPIView):
    serializer_class = FCMDeviceSerializer


# API PARA ENCONTRAR MASCOTA PREMIUM
@api_view(['POST'])
def find_pet_premium(request):
    # obtener la mascota en base al microchip
    mascota_perdida = MascotaPremium.objects.get(microchip=request.data['microchip'])
    print(mascota_perdida)
    # obtener el usuario relacionado a esa mascota
    usuario_mascota = Usuario.objects.get(mascota__nombre=mascota_perdida)
    print(usuario_mascota)
    # usuario = Usuario.objects.get(id=usuario_mascota)

    titulo = "CorazónPet"
    mensaje = "¡Un usuario ha encontrado tu mascota, pronto nos pondremos en contacto contigo!"

    fcm_obj = FCMDevice.objects.get(device_id=usuario_mascota.email)
    if fcm_obj.type == "ios":
        fcm_obj.send_message(title=titulo, body=mensaje, sound='default')

    elif fcm_obj.type == "android":
        fcm_obj.send_message(data={'titulo': titulo, 'mensaje': mensaje})

    return Response({'data': 'Notificacion enviada'}, status=status.HTTP_201_CREATED)
