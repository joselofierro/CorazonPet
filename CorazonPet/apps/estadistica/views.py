from django.shortcuts import render

# Create your views here.
from apps.ciudad.models import Ciudad
from apps.historial_vacuna.models import HistorialVacuna
from apps.mascota.models import Mascota
from apps.mascota_perdida.models import MascotaPerdida
from apps.mascota_premium.models import MascotaPremium
from apps.raza.models import Raza
from apps.tipo_mascota.models import TipoMascota


def mascotas_ciudad(request):
    ciudad = Ciudad.objects.all()
    mascotas = Mascota.objects.all().count()

    contexto = {"labels": ciudad, "datos": [mascotas], "titulo": "Mascotas por ciudad", "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def mascota_genero(request):
    mascota_macho = Mascota.objects.filter(sexo='M').count()
    mascota_hembra = Mascota.objects.filter(sexo='F').count()
    labels = ['Macho', 'Hembra']
    contexto = {"labels": labels, "datos": [mascota_macho, mascota_hembra], "titulo": "Género de mascotas",
                "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def tipo_mascota(request):
    labels = TipoMascota.objects.all()

    numero_tipo_mascota = Mascota.objects.all().count()

    contexto = {"labels": labels, "datos": [numero_tipo_mascota], "titulo": "Tipo de mascota", "tipo": "bar"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def razas_mascota(request):
    mascotas = Mascota.objects.all()
    razas = Mascota.objects.all().count()
    for mascota in mascotas:
        labels = Raza.objects.filter(mascota=mascota)

        contexto = {"labels": labels, "datos": [razas], "titulo": "Raza de mascotas", "tipo": "bar"}

        return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def esterilizados(request):
    labels = ["Macho", "Hembra"]

    estelizado_macho = Mascota.objects.filter(esterilizado=True, sexo="M").count()
    estelizado_hembra = Mascota.objects.filter(esterilizado=True, sexo="F").count()

    contexto = {"labels": labels, "datos": [estelizado_macho, estelizado_hembra], "titulo": "Mascotas Esterilizadas",
                "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def vacunados(request):
    labels = ["Macho", "Hembra"]

    mascota_vacuna_hembra = HistorialVacuna.objects.filter(mascota__sexo="F").count()
    mascota_vacuna_macho = HistorialVacuna.objects.filter(mascota__sexo="M").count()

    contexto = {"labels": labels, "datos": [mascota_vacuna_hembra, mascota_vacuna_macho],
                "titulo": "Mascotas vacunadas", "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def mascotas_poliza(request):
    labels = ["Animales con poliza"]

    poliza = Mascota.objects.filter(numero_poliza__isnull=False).count()

    contexto = {"labels": labels, "datos": [poliza], "Titulo": "Animales con poliza", "tipo": "bar"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def mascotas_microchip(request):
    labels = ["Mascota con Microchip"]
    mascotas_premium = MascotaPremium.objects.filter(microchip__isnull=False).count()

    contexto = {"labels": labels, "datos": [mascotas_premium], "Titulo": "Identificación", "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')
