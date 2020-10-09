from django.db import connection
from datetime import datetime
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
            'imagen':str(base64.b64encode(fila[8].read()), 'utf-8')
        }

        lista.append(data)

    return lista

# METODOS PARA AGREGAR UN COMERCIANTE EN PAGINA DE REGISTRO
def agregar_comerciante(run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_COMERCIANTE', [run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna, salida])
    return salida.getvalue()


def listar_regiones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_REGIONES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def validaRegistroRut(run):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaR = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_BUSCA_RUT", [run, salidaR])
    return salidaR.getvalue()

def validaRegistroEmail(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaC = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_BUSCA_EMAIL", [correo, salidaC])
    return salidaC.getvalue()   

# METODOS PARA ACCEDER AL SISTEMA EN LOGIN DE USUARIO COMERCIANTE

def accesoComerciante():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_ACCSESO_USUARIO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista