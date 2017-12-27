from django.db.models import Q
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
    ciudades = Ciudad.objects.all().values_list('nombre', flat=True)
    list_ciudad = []
    for ciudad in ciudades:
        list_ciudad.append(Mascota.objects.filter(usuario__ciudad__nombre=ciudad).count())

    contexto = {"labels": ciudades, "datos": [list_ciudad], "titulo": "Mascotas por ciudad", "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def mascota_genero(request):
    mascota_macho = Mascota.objects.filter(sexo='M').count()
    mascota_hembra = Mascota.objects.filter(sexo='F').count()
    labels = ['Macho', 'Hembra']
    contexto = {"labels": labels, "datos": [mascota_macho, mascota_hembra], "titulo": "Género de mascotas",
                "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def tipo_mascota(request):
    labels = TipoMascota.objects.all().values_list('nombre', flat=True)

    lista_dato = []

    for tp in labels:
        lista_dato.append(Mascota.objects.filter(raza__tipo_mascota__nombre=tp).count())

    contexto = {"labels": labels, "datos": lista_dato, "titulo": "Tipo de mascota", "tipo": "bar"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def razas_mascota_perro(request):
    mascotas = Mascota.objects.filter(raza__tipo_mascota__nombre="Perro")

    labels = []
    datos = []

    for mascota in mascotas:
        labels.append(mascota.raza.nombre)

    for raza in labels:
        datos.append(Mascota.objects.filter(raza__nombre=raza).count())

    contexto = {"labels": labels, "datos": datos, "titulo": "Raza de perros", "tipo": "bar"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def razas_mascota_gato(request):
    # mascotas por el tipo de mascota = GATO
    mascotas = Mascota.objects.filter(raza__tipo_mascota__nombre="Gato")
    labels = []
    datos = []
    # recorremos las mascotas agregamos al listado el nombre de raza que existen
    for mascota in mascotas:
        labels.append(mascota.raza.nombre)
    #
    for raza in labels:
        datos.append(Mascota.objects.filter(raza__nombre=raza).count())

    contexto = {"labels": labels, "datos": datos, "titulo": "Raza de perros", "tipo": "bar"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def esterilizados(request):
    labels = ["Macho", "Hembra"]

    estelizado_macho = Mascota.objects.filter(Q(esterilizado=True) & Q(sexo="M")).count()
    estelizado_hembra = Mascota.objects.filter(Q(esterilizado=True) & Q(sexo="F")).count()

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
    labels = ["Animales con poliza", "Animales sin poliza"]

    poliza_con = Mascota.objects.filter(~Q(numero_poliza='')).count()
    poliza_sin = Mascota.objects.filter(numero_poliza='').count()

    contexto = {"labels": labels, "datos": [poliza_con, poliza_sin], "Titulo": "Animales con poliza", "tipo": "bar"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')


def mascotas_microchip(request):
    labels = ["Mascota con Microchip"]
    mascotas_premium = MascotaPremium.objects.all().count()

    contexto = {"labels": labels, "datos": [mascotas_premium], "Titulo": "Identificación", "tipo": "pie"}

    return render(request, 'estadistica/estadisticas.html', contexto, content_type='text/html')
