from django.shortcuts import render
from django.db import connection
from datetime import date
import cx_Oracle
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

# METODOS PARA ACCEDER A DATOS DEL PLSQL


def listar_saldos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SALDOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def listar_saldos_calidad_alta():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LS_CALIDAD_ALTA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def saldos_calidad_alta_media():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LS_CALIDAD_BAJA_MEDIA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def listar_por_regiones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_POR_REGIONES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def listar_detallesaldos(detalle_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_DETALLE_VLOCAL", [detalle_id, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def agregar_comerciante(RUN_USUARIO, NOMBRE, AP_PATERNO, AP_MATERNO, FECHA_NAC, EMAIL, DIRECCION, NUM_CELULAR, CLAVE, ID_COMUNA):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    ID_ESTADO = 1
    ID_ROL = 3
    ID_GENERO = 1
    ID_EMPRESA = 0
    cursor.callproc('SP_REGISTRO_COMERCIANTES', [RUN_USUARIO, NOMBRE, AP_PATERNO, AP_MATERNO, FECHA_NAC,
                                                 EMAIL, DIRECCION, NUM_CELULAR, CLAVE, ID_ESTADO, ID_COMUNA, ID_ROL, ID_GENERO, ID_EMPRESA])
    return salida.getvalue()

# def detalle(request,detalle_id):#detalle_id
  #  print(listar_detallesaldos(detalle_id))
   # data = {
   #     'BD_VLOCAL':listar_detallesaldos(detalle_id)
  #  }
  #  tituloPagina = 'Manzana Candy'
  #  precio = '{:,}'.format(1990).replace(',','.')
  #  cantidad = '1'
   # return render(request, 'detalle.html', { 'tituloPagina' : tituloPagina, 'precio' : precio, 'cantidad' : cantidad })
