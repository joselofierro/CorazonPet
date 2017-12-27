from django.shortcuts import render


# Create your views here.
def restablecer_password(request, token):
    if request.method == "GET":
        return render(request, 'mail_templates/app_recuperar_contrasena.html', {"token": token})

