from django.shortcuts import render
from django.db import connection
from datetime import date
import cx_Oracle
from .metodos_views import *

# Create your views here. la funcion def home busca el template (controlador)


def home(request):
    # print(listar_saldos_calidad_alta())
    print(saldos_calidad_alta_media())
    data = {
        'ca_alta': listar_saldos_calidad_alta(),
        'ca_baja_media': saldos_calidad_alta_media()
    }
    return render(request, 'index.html', data)


def login(request):
    tituloPagina = 'Ingreso'
    return render(request, 'login.html', {'tituloPagina': tituloPagina})


def registro(request):
    #fechaActual = date.today()
    print(listar_por_regiones())  # ver listado en consola
    data = {
        'region': listar_por_regiones()
    }

    if request.method == 'POST':
        ru = request.POST.get('registro-rut')
        nombre = request.POST.get('registro-nombre')
        paterno = request.POST.get('registro-Paterno')
        materno = request.POST.get('registro-materno')
        f_nac = request.POST.get('registro-fecha')
        email = request.POST.get('registro-correo')
        direccion = request.POST.get('registro-direccion')
        celular = request.POST.get('registro-celular')
        clave = request.POST.get('registro-rut')
        comuna = request.POST.get('registro-comuna')
        salida = agregar_comerciante(
            ru, nombre, paterno, materno, f_nac, email, direccion, celular, clave, comuna)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'El registro no se agregó'

    return render(request, 'registro.html', data)


def crearSolicitud(request):

    return render(request, 'crearSolicitud.html')


def detalle(request, detalle_id):
    # print(listar_detallesaldos(detalle_id))
    data = {
        'db_vlocal': listar_detallesaldos(detalle_id)
    }

    return render(request, 'detalle.html', data)


def portalSaldos(request):
    # print(listar_saldos())#ver listado en consola
    data = {
        'saldos': listar_saldos()
    }
    return render(request, 'portalSaldos.html', data)
