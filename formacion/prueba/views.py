
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .models import Aprendiz
from .forms import AprendizForm


# =====================================
# CONVERTIR DIRECCION EN COORDENADAS
# =====================================

def obtener_coordenadas(direccion):

    url = 'https://nominatim.openstreetmap.org/search'

    parametros = {
        'q': direccion,
        'format': 'jsonv2',
        'limit': 1
    }

    encabezados = {
        'User-Agent': 'CentroFormacionSENA/1.0'
    }

    try:
        respuesta = requests.get(
            url,
            params=parametros,
            headers=encabezados,
            timeout=10
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

        if datos:
            latitud = float(datos[0]['lat'])
            longitud = float(datos[0]['lon'])

            return latitud, longitud

        return None, None

    except (requests.exceptions.RequestException, ValueError, KeyError):
        return None, None


# =====================================
# LISTAR APRENDICES
# =====================================

def lista_aprendices(request):

    aprendices = Aprendiz.objects.all()

    contexto = {
        'aprendices': aprendices
    }

    return render(request, 'prueba/index.html', contexto)


# =====================================
# CREAR APRENDIZ
# =====================================

def crear_aprendiz(request):

    form = AprendizForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        aprendiz = form.save(commit=False)

        # Consultar la ubicación de la dirección
        if aprendiz.direccion:
            latitud, longitud = obtener_coordenadas(
                aprendiz.direccion
            )

            aprendiz.latitud = latitud
            aprendiz.longitud = longitud

        aprendiz.save()

        messages.success(
            request,
            'El aprendiz fue creado correctamente.'
        )

        if aprendiz.direccion and aprendiz.latitud is None:
            messages.warning(
                request,
                'El aprendiz fue guardado, pero no se pudo encontrar su dirección en el mapa.'
            )

        return redirect('listar_aprendices')

    return render(request, 'prueba/crear_aprendiz.html', {
        'form': form
    })


# =====================================
# EDITAR APRENDIZ
# =====================================

def editar_aprendiz(request, documento):

    aprendiz = get_object_or_404(
        Aprendiz,
        documento=documento
    )

    if request.method == 'POST':

        direccion_anterior = aprendiz.direccion

        form = AprendizForm(
            request.POST,
            instance=aprendiz
        )

        form.fields['documento'].disabled = True

        if form.is_valid():

            aprendiz = form.save(commit=False)

            # Actualizar coordenadas si cambia la dirección
            if aprendiz.direccion != direccion_anterior:

                latitud, longitud = obtener_coordenadas(
                    aprendiz.direccion
                )

                aprendiz.latitud = latitud
                aprendiz.longitud = longitud

            aprendiz.save()

            messages.success(
                request,
                'Aprendiz editado correctamente.'
            )

            if aprendiz.direccion and aprendiz.latitud is None:
                messages.warning(
                    request,
                    'No se pudo encontrar la nueva dirección en el mapa.'
                )

            return redirect('listar_aprendices')

    else:

        form = AprendizForm(instance=aprendiz)
        form.fields['documento'].disabled = True

    return render(request, 'prueba/formulario.html', {
        'form': form,
        'titulo': f'Editar {aprendiz.nombre} - {aprendiz.apellido}',
        'aprendiz': aprendiz
    })


# =====================================
# ELIMINAR APRENDIZ
# =====================================

def eliminar_aprendiz(request, documento):

    aprendiz = get_object_or_404(
        Aprendiz,
        documento=documento
    )

    if request.method == 'POST':

        aprendiz.delete()

        messages.success(
            request,
            'Se eliminó el usuario correctamente.'
        )

        return redirect('listar_aprendices')

    return render(request, 'prueba/eliminar.html', {
        'aprendiz': aprendiz
    })


# =====================================
# VERIFICAR SI ES ADMINISTRADOR
# =====================================

def es_administrador(usuario):
    return usuario.is_authenticated and usuario.is_staff


# =====================================
# MAPA DE APRENDICES
# SOLO PARA ADMINISTRADORES
# =====================================

@user_passes_test(es_administrador, login_url='/admin/login/')
def mapa_aprendices(request):
    aprendices = Aprendiz.objects.exclude(
        latitud__isnull=True
    ).exclude(
        longitud__isnull=True
    )

    ubicaciones = []

    for aprendiz in aprendices:
        ubicaciones.append({
            'latitud': aprendiz.latitud,
            'longitud': aprendiz.longitud
        })

    return render(request, 'prueba/mapa.html', {
        'ubicaciones': ubicaciones,
        'total_ubicaciones': len(ubicaciones)
    })