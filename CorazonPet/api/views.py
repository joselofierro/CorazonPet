import base64
import json
import time

from django.contrib.auth.models import User

from django.template.loader import render_to_string
from fcm_django.api.rest_framework import FCMDeviceSerializer
from fcm_django.models import FCMDevice
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *
from api.serializers import *
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authentication import TokenAuthentication
import hashlib

# API con el listado de tipos de mascota y su respectiva razas
from apps.usuario.models import RecuperarContrasena


class TipoMascotaAPI(ListAPIView):
    serializer_class = TipoMascotaSerializer

    def get_queryset(self):
        return TipoMascota.objects.all().order_by('nombre')


@api_view(['post'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def crear_raza(request):
    # recorremos el json que viene del post, una vez terminado el ciclo rexspondemos con un 200
    for mascota in request.data:
        serializer = CreateManyRazasSerializer(data=mascota)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'data': 'razas creada'}, status=status.HTTP_200_OK)


class ListadoMascotaApi(ListAPIView):
    serializer_class = RazaSerializer

    def get_queryset(self):
        return Raza.objects.filter(tipo_mascota=self.kwargs['id']).order_by('nombre')


# API PARA CREAR USUARIO
class CreateUser(CreateAPIView):
    serializer_class = CreateUserSerializer

    def get_queryset(self):
        return Usuario.objects.all()

    def post(self, request, **kwargs):
        try:
            usuario = Usuario.objects.get(email=request.data['email'])
            token = Token.objects.get(user=usuario.user_token)
            usuario_serializer = CreateUserSerializer(usuario)
            # guardamos la data en una variable
            json_serializer = usuario_serializer.data
            # eliminamos el campo user_token
            json_serializer.pop('user_token')
            # agregamos el campo token con la llave del token
            json_serializer['token'] = token.key
            return Response(json_serializer, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            usuario_serializer = CreateUserSerializer(data=request.data)
            if usuario_serializer.is_valid():
                # Crear el usuario Django (User)
                usuario = User.objects.create(
                    first_name=request.data['nombre'],
                    last_name=request.data['apellido'],
                    username=request.data['nombre'],
                    email=request.data['email'])

                # Creamos el token
                token = Token.objects.create(user=usuario)

                # instanciamos el serializer del usuario
                usuario_obj = usuario_serializer.save()
                # pasamos al usuario el User
                usuario_obj.user_token = usuario

                # Guardamos contraseña encriptada
                if 'contrasena' in request.data:
                    contrasena = request.data['contrasena']
                    if contrasena != "":
                        contrasena_cifrada = make_password(contrasena, salt=None, hasher='sha1')
                        usuario_obj.contrasena = contrasena_cifrada

                # guardamos la instancia con la pass y el User
                usuario_obj.save()
                # instanciamos el nuevo serializer
                usuario_serializer = CreateUserSerializer(usuario_obj)
                # guardamos la data en una variable
                json_serializer = usuario_serializer.data
                # eliminamos el campo user_token
                json_serializer.pop('user_token')
                # agregamos el campo token con la llave del token
                json_serializer['token'] = token.key
                return Response(json_serializer, status=status.HTTP_201_CREATED)
            else:
                return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
def login(request):
    if request.method == 'POST':
        try:
            email = request.data['email']
            password = request.data['pass']
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.contrasena):
                serializer = CreateUserSerializer(usuario, many=False)
                # instanciamos la data del json
                user_data = serializer.data
                # obtenemos el token del User
                token = Token.objects.get(user=usuario.user_token)
                # al campo token le ponemos la llave del token
                user_data['token'] = token.key
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                return Response({'data': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)
        except Usuario.DoesNotExist:
            return Response({'data': 'No existe usuario con este email'}, status=status.HTTP_400_BAD_REQUEST)


# API de listado de usuario por correo
class ListUserByCorreo(APIView):
    def get(self, request, email):
        try:
            user_obj = Usuario.objects.get(email=email)
            user_serializer = ListUserByParameter(user_obj)
            user_data = user_serializer.data
            token = Token.objects.get(user=user_obj.user_token)
            user_data['token'] = token.key
            return Response(user_data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'data': 'No existe usuario con ese correo'}, status=status.HTTP_404_NOT_FOUND)


# API PARA REPORTAR MASCOTAS PERDIDAS Y LISTAR MASCOTAS PERDIDAS
class PetLostApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        mascota_perdida_serializer = ReportarMascotaPremiumSerializer(data=request.data)
        if mascota_perdida_serializer.is_valid():
            titulo = "CorazónPet"
            mensaje = "Una mascota ha sido reportada como perdida. ¡Ingresa a la nuestra app y ayúdanos a encontrarla! 🐕"
            mascota_perdida_serializer.save()

            mascota_perdida = MascotaPerdida.objects.get(mascota_id=request.data['mascota'])

            mascota_perdida_serializer = MascotaPerdidaSerializer(mascota_perdida, many=False,
                                                                  context={'request': request})
            # Obtenemos los usuarios Android
            usuarios_android = FCMDevice.objects.filter(type='android')

            # Enviamos la notificacion
            usuarios_android.send_message(data={
                "type": "MEASURE_CHANGE",
                "custom_notification": {
                    "body": mensaje,
                    "title": titulo,
                    "priority": "high",
                    "icon": "ic_notification_silueta",
                    "show_in_foreground": True,
                    "id": "1",
                    "large_icon": "ic_launcher",
                    "big_text": mensaje,
                    "sound": "default",
                    "lights": True,
                    "mascota_perdida": json.dumps(mascota_perdida_serializer.data)
                }
            })

            # Obtenemos los usuarios ios
            usuarios_ios = FCMDevice.objects.filter(type='ios')
            # Enviamos la notificacion
            usuarios_ios.send_message(title=titulo, body=mensaje, sound='default', data={
                "mascota_perdida": mascota_perdida_serializer.data
            })
            return Response(mascota_perdida_serializer.data, status=status.HTTP_201_CREATED)
        return Response(mascota_perdida_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    serializer_class = VacunaSerializer

    def get_queryset(self):
        return Vacuna.objects.all().order_by('nombre')


# API PARA CREAR VACUNA A LA MASCOTA EN HISTORIAL VACUNA
class CreateHistorialVacuna(CreateAPIView):
    serializer_class = AddVacunaHistorial
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# Listado de historias de vacunas por el id de la mascota
class ListHistorialVacunaApi(ListAPIView):
    serializer_class = HistorialVacunaSerializer

    def get_queryset(self):
        return HistorialVacuna.objects.filter(mascota__id=self.kwargs['pk'])


# API PARA CREAR MEDICAMENTO A LA MASCOTA EN EL HISTORIAL MEDICO
class CreateHistorialMedicamento(CreateAPIView):
    serializer_class = AddHistorialMedicamento
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        historial_medicamento = AddHistorialMedicamento(data=request.data)
        if historial_medicamento.is_valid():
            img_64 = request.data['imagen']
            obj_historial_medicamento = historial_medicamento.save()
            if img_64 != '':
                img_deco = base64.b64decode(img_64)
                obj_historial_medicamento.imagen = ContentFile(img_deco,
                                                               name='medicamento_' + obj_historial_medicamento.mascota.nombre + "_" + str(
                                                                   obj_historial_medicamento.mascota.id) + "_" + obj_historial_medicamento.medicamento + '.jpg')
                obj_historial_medicamento.save()
            return Response({'data': 'Medicamento creado'}, status=status.HTTP_201_CREATED)
        return Response({'error': historial_medicamento.errors}, status=status.HTTP_400_BAD_REQUEST)


# HISTORIAL MEDICO POR EL ID DE LA MASCOTA
class ListHistorialMedicamentoApi(ListAPIView):
    serializer_class = HistorialMedicamentoSerializer

    def get_queryset(self):
        return HistorialMedicamento.objects.filter(mascota=self.kwargs['pk'])


# API PARA CREAR RECORDATORIO
class CreateRecordatorio(CreateAPIView):
    serializer_class = CreateRecordatorioSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# API PARA RELACIONAR LOS IDENTIFICADORES DE LOS RECORDATORIOS
class CreateIdentifierRecordatorio(CreateAPIView):
    serializer_class = CreateIdentifierRecordatorioSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# listado de recordatorio por el id de la mascota
class ListRecordatorioApi(ListAPIView):
    serializer_class = RecordatorioSerializer

    def get_queryset(self):
        return Recordatorio.objects.filter(mascota__id=self.kwargs['pk'])


# API PARA CREAR MASCOTAS
class CreateMascotaApi(CreateAPIView):
    serializer_class = CreateMascotaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def status_recordatorio(request):
    try:
        recordatorio = request.data['recordatorio']

        estado = request.data['estado']

        recordatorio_obj = Recordatorio.objects.get(id=recordatorio)

        recordatorio_obj.completado = estado

        recordatorio_obj.save()

        return Response({'data': 'Actualizado'}, status=status.HTTP_200_OK)

    except Recordatorio.DoesNotExist:
        return Response({'data': 'Recordatorio no existe'}, status=status.HTTP_404_NOT_FOUND)


# API PARA GENERAR MASCOTA PREMIUM
class MascotaPremiumAPI(CreateAPIView):
    serializer_class = MascotaPremiumSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# Api para crear las notificaciones
class CreateFCM(CreateAPIView):
    serializer_class = FCMDeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# API PARA ENCONTRAR MASCOTA PREMIUM
@api_view(['post'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def find_pet_premium(request):
    # obtener la mascota en base al microchip
    mascota_perdida = MascotaPremium.objects.get(microchip=request.data['microchip'])
    print(mascota_perdida)
    # obtener el usuario relacionado a esa mascota
    usuario_mascota = Usuario.objects.get(mascota__nombre=mascota_perdida)
    print(usuario_mascota)

    titulo = "CorazónPet"
    mensaje = "¡Un usuario ha encontrado tu mascota, pronto nos pondremos en contacto contigo!"
    # obtenemos el usuario en el FCMDEVICE por el email
    fcm_obj = FCMDevice.objects.filter(device_id=usuario_mascota.email)
    for fcm in fcm_obj:
        if fcm.type == "ios":
            fcm.send_message(title=titulo, body=mensaje, sound='default')
        elif fcm.type == "android":
            fcm.send_message(data={
                "type": "MEASURE_CHANGE",
                "custom_notification": {
                    "body": mensaje,
                    "title": titulo,
                    "priority": "high",
                    "icon": "ic_notification_silueta",
                    "show_in_foreground": True,
                    "id": "1",
                    "large_icon": "ic_launcher",
                    "big_text": mensaje,
                    "sound": "default",
                    "lights": True,
                }
            })

    # Llegaran por parametros los atributos: latitud, longitud, telefono, microchip
    msg = render_to_string('mail_templates/EncontroMascotaPremium.html', {
        'numero': request.data['telefono'],
        'mascota': mascota_perdida.mascota.nombre,
        'usuario': usuario_mascota.id,
        'latitud': request.data['latitud'],
        'longitud': request.data['longitud'],
    })

    send_mail(
        'Han encontrado una mascota premium',
        'Mensaje',
        'backend.corazon@gmail.com',
        ['giussepr@gmail.com'],
        html_message=msg)

    return Response({'data': 'Notificacion enviada'}, status=status.HTTP_201_CREATED)


# API PARA REFUGIAR MASCOTA PERDIDA CALLE
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def refugiarPerdido(request):
    if request.method == "POST":
        # Llegaran por parametros los atributos de mascota calle: id, imagen, tiempo, numero, nombre
        msg = render_to_string('mail_templates/RefugiarCalle.html', {
            'usuario': request.data['nombre'],
            'id': request.data['id'],
            'dias': request.data['tiempo'],
            'numero': request.data['numero']
        })
        send_mail(
            'Alguien quiere refugiar una mascota',
            'Mensaje',
            'backend.corazon@gmail.com',
            ['diana.sendoya@gmail.com', 'juanpps78@gmail.com'],
            html_message=msg)
        return Response({'data': 'Gracias'}, status=status.HTTP_200_OK)
    else:
        return Response({'¿Que haces?': 'Ola k ace, chismoseando o que hace? 👽🐫'})


# API PARA QUE USUARIO CREE VACUNAS
class CreateVacunaUsuarioAPI(CreateAPIView):
    serializer_class = CVacunaUsuarioSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # si ya existe vacuna con ese nombre
        if VacunaUsuario.objects.filter(nombre=request.data['nombre']).exists():
            return Response({'data': 'Vacuna ya existe con ese nombre'}, status=status.HTTP_200_OK)
        else:
            vacuna_obj_serial = CVacunaUsuarioSerializer(data=request.data)
            if vacuna_obj_serial.is_valid():
                vacuna_obj_serial.save()
                return Response({'data': 'Vacuna creada'}, status=status.HTTP_201_CREATED)
            return Response({'data': vacuna_obj_serial.errors}, status=status.HTTP_400_BAD_REQUEST)


# API CON LISTADO DE VACUNAS CREADAS POR EL USUARIO
class VacunaUsuarioAPI(ListAPIView):
    serializer_class = VacunaUsuarioSerializer

    def get_queryset(self):
        # filtramos las vacunas creadas por el id del usuario
        return VacunaUsuario.objects.filter(usuario=self.kwargs['id_user']).order_by('nombre')


# API GENERICA QUE ACTUALIZA O ELIMINAR LAS VACUNAS POR SU ID
class GVacunaUsuarioAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_obj_vacuna(self, pk):
        try:
            return VacunaUsuario.objects.get(id=pk)
        except VacunaUsuario.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        vacuna_obj = self.get_obj_vacuna(pk)
        serializer = CVacunaUsuarioSerializer(vacuna_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vacuna_obj = self.get_obj_vacuna(pk)
        vacuna_obj.delete()
        return Response({'data': 'Vacuna eliminada'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_vacuna_usuario(request):
    if request.method == 'POST':
        try:
            ids = request.data['ids']
            for ind_id in ids:
                VacunaUsuario.objects.get(id=ind_id).delete()
            return Response({'data': "Vacuna usuario eliminada"}, status=status.HTTP_200_OK)
        except VacunaUsuario.DoesNotExist:
            return Response({'error': 'No se ha podido eliminar la vacuna'}, status=status.HTTP_400_BAD_REQUEST)


# API GENERICA PARA ACTUALIZAR Y ELIMINAR UNA MASCOTA
class GMascotaUserAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_obj_mascota(self, pk):
        try:
            return Mascota.objects.get(id=pk)
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj_mascota = self.get_obj_mascota(pk)
        serializer = MascotaUserSerializer(obj_mascota, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        obj_mascota = self.get_obj_mascota(pk)
        serializer = GMascotaUserSerializer(obj_mascota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj_mascota = self.get_obj_mascota(pk)
        obj_mascota.delete()
        return Response({'data': 'Mascota eliminada'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def cambio_foto_mascota(request):
    try:
        id_mascota = request.data['id']
        imagen_64 = request.data['imagen']

        imagen_decode = base64.b64decode(imagen_64)

        obj_mascota = Mascota.objects.get(id=id_mascota)

        obj_mascota.foto_perfil = ContentFile(imagen_decode, name='imagen_mascota_' + obj_mascota.nombre + "_" + str(
            obj_mascota.id) + '.jpg')

        obj_mascota.save()

        return Response({'data': 'Imagen actualizada'}, status=status.HTTP_200_OK)
    except Mascota.DoesNotExist:
        return Response({'data': 'Mascota no existe'}, status=status.HTTP_404_NOT_FOUND)


# API PARA ELIMINAR FOTO DE MASCOTA
@api_view(['delete'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def eliminar_foto_mascota(request, pk):
    try:
        obj_media = ImagenesMascota.objects.get(id=pk)
        obj_media.delete()
        return Response({'data': 'Imagen eliminada'}, status=status.HTTP_204_NO_CONTENT)
    except ImagenesMascota.DoesNotExist:
        return Response({'data': 'Imagen no existe'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def eliminar_reporte_mascota_perdida(request, pk):
    try:
        obj_mascota_perdida = MascotaPerdida.objects.get(id=pk)
        obj_mascota_perdida.delete()
        return Response({'data': 'Reporte eliminado'}, status=status.HTTP_204_NO_CONTENT)
    except MascotaPerdida.DoesNotExist:
        return Response({'data': 'Reporte no existe'}, status=status.HTTP_400_BAD_REQUEST)


class GHistorialVacunaApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def obj_historial_vacuna(self, pk):
        try:
            return HistorialVacuna.objects.get(id=pk)
        except HistorialVacuna.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        obj_historial_vacuna = self.obj_historial_vacuna(pk)
        serializer = GHistorialVacunaSerializer(obj_historial_vacuna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj_historial_vacuna = self.obj_historial_vacuna(pk)
        obj_historial_vacuna.delete()
        return Response({'data': 'Historial de vacuna eliminado'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['put'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def cambiar_foto_medicamento(request, pk):
    try:
        obj_medicamento = HistorialMedicamento.objects.get(id=pk)
        imagen = base64.b64decode(request.data['imagen'])

        obj_medicamento.imagen = ContentFile(imagen,
                                             name='imagen_medicamento_' + obj_medicamento.mascota.nombre + '.jpg')

        obj_medicamento.save()

        return Response({'data': 'Imagen actualizada'}, status=status.HTTP_200_OK)
    except HistorialMedicamento.DoesNotExist:
        return Response({'error': 'No existe historial'}, status=status.HTTP_400_BAD_REQUEST)


# API GENERICA PARA ACTUALIZAR Y ELIMINAR MEDICAMENTOS
class GHistorialMedicamentoApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def obj_historial_medicamento(self, pk):
        try:
            return HistorialMedicamento.objects.get(id=pk)
        except HistorialMedicamento.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        obj_historial_medicamento = self.obj_historial_medicamento(pk)
        serializer = GHistorialMedicamentoSerializer(obj_historial_medicamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj_historial_medicamento = self.obj_historial_medicamento(pk)
        obj_historial_medicamento.delete()
        return Response({'data': 'Historial de vacuna eliminado'}, status=status.HTTP_204_NO_CONTENT)


# API GENERICA PARA ACTUALIZAR Y ELIMINAR RECORDATORIO
class GRecordatorioApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def obj_recordatorio(self, pk):
        try:
            return Recordatorio.objects.get(id=pk)
        except Recordatorio.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        obj_recordatorio = self.obj_recordatorio(pk)
        serializer = RecordatorioSerializer(obj_recordatorio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj_recordatorio = self.obj_recordatorio(pk)
        obj_recordatorio.delete()
        return Response({'data': 'Recordatorio eliminado'}, status=status.HTTP_204_NO_CONTENT)


# API PARA LISTADO DE CIUDADES
class CiudadesApi(ListAPIView):
    serializer_class = CiudadSerializer

    def get_queryset(self):
        return Ciudad.objects.all().order_by('nombre')


@api_view(['post'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def generatevolante(request):
    try:
        obj_mascota = MascotaPerdida.objects.get(id=request.data['id'])

        img_64 = request.data['volante']
        img_deco = base64.b64decode(img_64)

        obj_mascota.volante = ContentFile(img_deco, name='imagen_mascota_' + obj_mascota.mascota.nombre + "_" + str(
            obj_mascota.mascota.id) + '.jpg')

        obj_mascota.save()
        return Response({'data': 'volante generado'}, status=status.HTTP_200_OK)
    except MascotaPerdida.DoesNotExist:
        return Response({'data': 'no found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getMascotaPerdidaByMicrochip(request, microchip):
    try:
        obj_mascota_premium = MascotaPremium.objects.get(microchip=microchip)
        obj_mascota_perdida = MascotaPerdida.objects.get(mascota=obj_mascota_premium.mascota)
        mascota_perdida_serializer = MascotaPerdidaSerializer(obj_mascota_perdida, many=False,
                                                              context={'request': request})
        return Response(mascota_perdida_serializer.data, status=status.HTTP_200_OK)
    except MascotaPremium.DoesNotExist:
        return Response({'data': "No existe mascota con este micrhochip"}, status=status.HTTP_404_NOT_FOUND)
    except MascotaPerdida.DoesNotExist:
        obj_mascota_premium = MascotaPremium.objects.get(microchip=microchip)
        serializer_mascota = MascotaUserSerializer(obj_mascota_premium.mascota, many=False,
                                                   context={'request': request})
        return Response(serializer_mascota.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def olvide_contrasena(request):
    if request.method == 'POST':
        try:
            # obtenemos el usuario por el email que llega
            usuario = Usuario.objects.get(email=request.data['email'])
            # si la contraseña es diferente de vacia
            if usuario.contrasena != '':
                # obtenemos la fecha de hoy
                fecha = time.strftime("%d/%m/%Y")
                # parseamos el email y la fecha a string con utf-8
                token = hashlib.sha1(str(usuario.email + "_" + fecha).encode('utf-8')).hexdigest()
                try:
                    # obtenemos el objeto recuperar contraseña por el email del user
                    RecuperarContrasena.objects.get(usuario__email=request.data['email'])
                    return Response({'data': 'Ya has solicitado recuperar contraseña'}, status=status.HTTP_200_OK)
                except RecuperarContrasena.DoesNotExist:
                    # creamos el registro en la tabla recuperar
                    RecuperarContrasena.objects.create(usuario=usuario, token=token)

                    msg = render_to_string('mail_templates/correo_recuperar_pass.html', {
                        'token': token
                    })

                    send_mail(
                        'Reestablecer contraseña corazónpet',
                        'Mensaje',
                        'backend.corazon@gmail.com',
                        [usuario.email],
                        html_message=msg)

                return Response({"data": "Te hemos enviado un email, sigue los pasos"}, status=status.HTTP_200_OK)
            else:
                return Response({'data': "Tu ingresas con Facebook"}, status=status.HTTP_404_NOT_FOUND)

        except Usuario.DoesNotExist:
            return Response({'data': "No existe usuario con este email"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def restablecer_password(request):
    if request.method == 'POST':
        token_data = request.data['token']
        # eliminamos el ultimo caracter del token
        token_data = token_data[:-1]
        new_pass = request.data['contrasena']

        try:
            # obtenemos el objeto de recuperar por el token que llega
            token_data = RecuperarContrasena.objects.get(token=token_data)
            # obtenemos la fecha de hoy
            fecha = time.strftime("%d/%m/%Y")
            # token de hoy con el email del registro
            token_hoy = hashlib.sha1(str(token_data.usuario.email + "_" + fecha).encode('utf-8')).hexdigest()

            # si lo solicitud el mismo dia
            if token_data.token == token_hoy:
                user_token = token_data.usuario
                user_token.contrasena = make_password(new_pass, salt=None, hasher='sha1')
                user_token.save()
                token_data.delete()
                return Response({'data': 'Tu contraseña se ha restablecido satisfactoriamente'},
                                status=status.HTTP_200_OK)
            else:
                token_data.delete()
                return Response({'data': 'Tu solicitud de restablecimiento ha caducado'},
                                status=status.HTTP_400_BAD_REQUEST)
        except RecuperarContrasena.DoesNotExist:
            return Response({'data': 'No se ha solicitado un restablecimiento de contraseña'},
                            status=status.HTTP_400_BAD_REQUEST)
