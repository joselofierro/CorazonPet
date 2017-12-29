import hashlib
import time

from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from apps.usuario.models import RecuperarContrasena


def restablecer_password(request, token):
    if request.method == "GET":
        """try:
            RecuperarContrasena.objects.get(token=token)
            return render(request, 'mail_templates/app_recuperar_contrasena.html', {"token": token})
        except RecuperarContrasena.DoesNotExist:
            return render(request, 'mail_templates/ContrasenaCambiada.html',
                          {'mensaje': 'No se ha solicitado restablecimiento de contraseña'})"""
        return render(request, 'mail_templates/app_recuperar_contrasena.html', {"token": token})
    elif request.method == "POST":
        token = request.POST.get('token')
        password = request.POST.get('pass')

        try:
            # obtenemos el objeto de recuperar por el token que llega
            token_data = RecuperarContrasena.objects.get(token=token)
            # obtenemos la fecha de hoy
            fecha = time.strftime("%d/%m/%Y")
            # token de hoy con el email del registro
            token_hoy = hashlib.sha1(str(token_data.usuario.email + "_" + fecha).encode('utf-8')).hexdigest()

            # si lo solicitud el mismo dia
            if token_data.token == token_hoy:
                user_token = token_data.usuario
                user_token.contrasena = make_password(password, salt=None, hasher='sha1')
                user_token.save()
                token_data.delete()
                return render(request, 'mail_templates/ContrasenaCambiada.html',
                              {'mensaje': 'Tu contraseña se ha restablecido satisfactoriamente'})
            else:
                token_data.delete()
                return render(request, 'mail_templates/ContrasenaCambiada.html',
                              {'mensaje': 'Tu solicitud de restablecimiento ha caducado'})
        except RecuperarContrasena.DoesNotExist:
            return render(request, 'mail_templates/ContrasenaCambiada.html',
                          {'mensaje': 'No se ha solicitado un restablecimiento de contraseña'})


def prueba(request):
    if request.method == "GET":
        return render(request, 'mail_templates/correo_recuperar_pass.html', {'usuario': 'Giussep'})
