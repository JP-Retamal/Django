from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime
from datetime import date
import cx_Oracle
import base64
# METODOS PARA ACCEDER A DATOS DEL PLSQL INDEX

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
            'imagen':str(base64.b64encode(fila[7].read()), 'utf-8')
        }

        lista.append(data)

    return lista


#PASAR DE INDEX A DETALLE DE TARGETA PUBLICACION DE VENTA LOCAL.
def listar_detallesaldos(detalle_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_DETALLE_VLOCAL", [detalle_id, out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[7].read()), 'utf-8')
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


# METODO PARA REALIZAR COMPRA DE PROMOCIÓN
def agregar_compra(descripcion, monto, fecha_pago, kilos, usuario, especie, variedad, idVentaLocal,  idStock):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PAGO', [descripcion, monto, fecha_pago, kilos, usuario, especie, variedad, idVentaLocal,  idStock, salida])
    return salida.getvalue()


# METODOS PARA ACCEDER AL SISTEMA EN LOGIN DE USUARIO COMERCIANTE

def validaCorreo(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    cursor.callproc("SP_VALIDA_CORREO", [correo, salida])
    return salida.getvalue()


def validaClave(clave, salida):

    if  clave==salida:
        print("valido")
        return True
    else:
        print("invalido")
        return False
    

def validaRol(correo, clave):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    cursor.callproc("SP_VALIDA_ROL", [correo, clave, salida])
    return salida.getvalue()
    

def rol(num):
    valor = int(num)-2
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    cursor.callproc("SP_BuscaRol", [valor, salida])
    return salida.getvalue()
    
def datosLogin(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_USUARIO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def userDjango(email, nombre, ap_paterno, clave):
    user = User.objects.create_user(username=email, first_name=nombre, last_name=ap_paterno, email=email, password=clave)
    user.is_staff = False
    user.groups.add(2)
    user.save()