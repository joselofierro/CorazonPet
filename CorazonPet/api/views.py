import base64
import jwt, json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from fcm_django.api.rest_framework import FCMDeviceSerializer
from fcm_django.models import FCMDevice
from django.core.mail import send_mail
from rest_framework.authentication import BaseAuthentication, get_authorization_header
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
class CreateUser(CreateAPIView):
    serializer_class = CreateUserSerializer

    def get_queryset(self):
        return Usuario.objects.all()

    def post(self, request, **kwargs):
        try:
            usuario = Usuario.objects.get(email=request.data['email'])
            print(usuario)
            usuario_serializer = CreateUserSerializer(usuario)
            return Response(usuario_serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            usuario_serializer = CreateUserSerializer(data=request.data)
            if usuario_serializer.is_valid():
                if 'contrasena' in request.data:
                    contrasena = request.data['contrasena']
                    if contrasena != "":
                        contrasena_cifrada = make_password(contrasena, salt=None, hasher='sha1')
                        usuario_obj = usuario_serializer.save()
                        usuario_obj.contrasena = contrasena_cifrada
                        usuario_obj.save()
                        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        usuario_serializer.save()
                        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    usuario_serializer.save()
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
            titulo = "CorazónPet"
            mensaje = "Una mascota ha sido reportada como perdida. ¡Ingresa a la nuestra app y ayúdanos a encontrarla! 🐕"

            # Obtenemos los usuarios Android
            usuarios_android = FCMDevice.objects.filter(type='android')

            # Enviamos la notificacion
            usuarios_android.send_message(data={'titulo': titulo, 'mensaje': mensaje})

            # Obtenemos los usuarios ios
            usuarios_ios = FCMDevice.objects.filter(type='ios')
            # Enviamos la notificacion
            usuarios_ios.send_message(title=titulo, body=mensaje, sound='default')

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
    serializer_class = VacunaSerializer

    def get_queryset(self):
        return Vacuna.objects.all().order_by('nombre')


# API PARA CREAR VACUNA A LA MASCOTA EN HISTORIAL VACUNA
class CreateHistorialVacuna(CreateAPIView):
    serializer_class = AddVacunaHistorial


# Listado de historias de vacunas por el id de la mascota
class ListHistorialVacunaApi(ListAPIView):
    serializer_class = HistorialVacunaSerializer

    def get_queryset(self):
        return HistorialVacuna.objects.filter(mascota__id=self.kwargs['pk'])


# API PARA CREAR MEDICAMENTO A LA MASCOTA EN EL HISTORIAL MEDICO
class CreateHistorialMedicamento(CreateAPIView):
    serializer_class = AddHistorialMedicamento

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
        return Response({'data': 'Recordatorio no existe'}, status=status.HTTP_404_NOT_FOUND)


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

    titulo = "CorazónPet"
    mensaje = "¡Un usuario ha encontrado tu mascota, pronto nos pondremos en contacto contigo!"
    # obtenemos el usuario en el FCMDEVICE por el email
    fcm_obj = FCMDevice.objects.filter(device_id=usuario_mascota.email)
    for fcm in fcm_obj:
        if fcm.type == "ios":
            fcm.send_message(title=titulo, body=mensaje, sound='default')
        elif fcm.type == "android":
            fcm.send_message(data={'titulo': titulo, 'mensaje': mensaje})

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
            ['giussepr@gmail.com'],
            html_message=msg)
        return Response({'data': 'Gracias'}, status=status.HTTP_200_OK)
    else:
        return Response({'¿Que haces?': 'Ola k ace, chismoseando o que hace? 👽🐫'})


# API PARA QUE USUARIO CREE VACUNAS
class CreateVacunaUsuarioAPI(CreateAPIView):
    serializer_class = CVacunaUsuarioSerializer

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
def eliminar_foto_mascota(request, pk):
    try:
        obj_media = ImagenesMascota.objects.get(id=pk)
        obj_media.delete()
        return Response({'data': 'Imagen eliminada'}, status=status.HTTP_204_NO_CONTENT)
    except ImagenesMascota.DoesNotExist:
        return Response({'data': 'Imagen no existe'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['delete'])
def eliminar_reporte_mascota_perdida(request, pk):
    try:
        obj_mascota_perdida = MascotaPerdida.objects.get(id=pk)
        obj_mascota_perdida.delete()
        return Response({'data': 'Reporte eliminado'}, status=status.HTTP_204_NO_CONTENT)
    except MascotaPerdida.DoesNotExist:
        return Response({'data': 'Reporte no existe'}, status=status.HTTP_400_BAD_REQUEST)


class GHistorialVacunaApi(APIView):
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


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("ASCII")  # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


# API PARA GENERAR JWT
class LoginTokenApi(APIView):
    def post(self, request, *args, **kwargs):

        # si no hay datos
        if not request.data:
            return Response({'Error': 'Digita el usuario/Contraseña'}, status=status.HTTP_400_BAD_REQUEST)

        # recibimos el user y el pass del User registrado
        username = request.data['username']
        password = request.data['password']

        try:
            # preguntamos por el user
            user_obj = User.objects.get(username=username)
            # chekeamos el password
            if user_obj.check_password(password):
                # autentificamos el usuario
                user_obj = authenticate(username=username, password=password)
        except User.DoesNotExist:
            return Response({'Error': 'Credenciales Invalidas'}, status=status.HTTP_400_BAD_REQUEST)

        # si hay un usuario, generamos el payload
        if user_obj:
            # generamos el payload(data)
            payload = {
                "id": user_obj.id,
                "email": user_obj.email
            }

            # codificamos el payload como una llave
            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
            print(jwt_token)

            print(json.dumps(jwt_token, cls=MyEncoder))

            # lo volvemos a formato json como una respuesta
            return HttpResponse(
                json.dumps(jwt_token, cls=MyEncoder), status=200, content_type="application/json"
            )

        else:
            return Response(
                json.dumps({'Error': 'Credenciales Invalidas'}), status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json")


class TokenAuthentication(BaseAuthentication):
    model = None

    def get_model(self):
        return User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Cabezera de token invalida'
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = 'Cabezera de token invalida'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = "Token nulo no almacenado"
                raise exceptions.AuthenticationFailed(msg)

        except UnicodeError:
            msg = "Token invalido, No debe contener caracteres invalidos"
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()
        payload = jwt.decode(token, "SECRET_KEY")
        id_user = payload['id']
        email = payload['email']
        msg = {'Error': "Token mismatch", 'status': "401"}
        try:

            user = User.objects.get(
                email=email,
                id=id_user,
                is_active=True
            )

            if not user.token['token'] == token:
                raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status="403")
        except User.DoesNotExist:
            return HttpResponse({'Error': "Internal server error"}, status="500")

        return user, token

    def authenticate_header(self, request):
        return 'Token'
