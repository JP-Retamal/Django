from django.db import connection
from datetime import date
import cx_Oracle
import base64
# METODOS PARA ACCEDER A DATOS DEL PLSQL

def listar_saldos_calidad_baja():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_CALIDAD_BAJA", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[7].read()), 'utf-8')
        }

        lista.append(data)

    return lista


def saldos_calidad_alta_media():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_CALIDAD_MEDIA_ALTA", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[7].read()), "utf-8")
        }

        lista.append(data)

    return lista


def listar_detallesaldos(detalle_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_DETALLE_VLOCAL", [detalle_id, out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[9].read()), 'utf-8')
        }

        lista.append(data)

    return lista


def agregar_comerciante(RUN_USUARIO, NOMBRE, AP_PATERNO, AP_MATERNO, FECHA_NAC, EMAIL, DIRECCION, NUM_CELULAR, CLAVE, ID_COMUNA, ID_GENERO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    ID_ESTADO = 1
    ID_ROL = 3 
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


def listar_por_regiones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_POR_REGIONES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
