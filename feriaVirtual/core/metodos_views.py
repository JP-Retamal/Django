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

def buscaComuna_id(comuna):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidacomuna = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_BUSCA_COMUNA", [comuna, salidacomuna])
    return salidacomuna.getvalue()

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
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_VALIDA_ROL", [correo, clave, salida])
    return salida.getvalue()
    

def rol(num):
    valor = int(num)-2
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    cursor.callproc("SP_BUSCAROL", [valor, salida])
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

def admin(user):
    return user.is_authenticated() and user.has_perm("view_ventalocal")


def listar_pedidos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PEDIDOS", [ out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[8].read()), 'utf-8')
        }

        lista.append(data)

    return lista


def lista_pedido():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_PEDIDO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def listar_detallePedidos(detalle_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_DETALLE_PEDIDO", [detalle_id, out_cur])

    lista = []  
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[8].read()), 'utf-8')
        }

        lista.append(data)

    return lista

def detalle_pedido_ofertar(detalle_id, variedad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_DETALLE_VARIEDAD", [detalle_id, variedad, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista



def listar_historial_compra(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_HISTORIAL_COMPRA", [correo,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listar_detalle_historial_compra(id_venta):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_DETALLE_HISTORIAL_COMPRA", [id_venta, out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[1].read()), 'utf-8')
        }

        lista.append(data)

    return lista

def listar_ofertas(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_HISTORIAL_OFERTA", [correo, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listar_detalle_historial_oferta(id_oferta):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_DETALLE_HISTORIAL_OFERTA", [id_oferta, out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }

        lista.append(data)

    return lista
#--modificar cuenta de usuario
def buscar_usuario(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_USUARIO", [correo, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def modificar_usuario( email, celular, direccion, comuna):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_USUARIO', [email, celular, direccion, comuna, salida])
    return salida.getvalue()


def agregarfruta(especie,variedad,cantidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc('sp_agregar_fruta',[especie,variedad,cantidad])

def listar_subcategorias_por_categoria(categoria_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("sp_listar_variedad_por_especies",[out_cur, categoria_id])

    lista=[]
    for fila in out_cur:
        lista.append(fila)
    
    return lista
    

def listar_especie():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("sp_listar_especie",[out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)
    
    return lista
# solicitudes admin aceptar, rechazar, ver.

def listar_solicitudes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SOLICITUDES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listar_detalle_solicitudes(id_detalle):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_DETALLE_SOLICITUDES", [id_detalle,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def aprobar_solicitud( id_detalle):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_APROBAR_SOLICITUD', [id_detalle, salida])
    return salida.getvalue()


def rechazar_solicitud( id_detalle):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_RECHAZAR_SOLICITUD', [id_detalle, salida])
    return salida.getvalue()

#------------------------------------------------------------

def listar_publicaciones_of_activas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_PUBLICACIONES_OFERTADAS",[out_cur])

    lista = []
    for fila in out_cur:
    #    data = {
    #        'data':fila,
    #        'imagen':str(base64.b64encode(fila[9].read()), 'utf-8')
    #    }

        #lista.append(data)
        lista.append(fila)

    return lista

def listar_detalle_publicaciones_of_activas(id_solicitud,especi, varied ):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_DETALLE_PUBLICACIONES_OFERTADAS",[id_solicitud, especi,varied,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listar_total_publicaciones_of_activas(id_solicitud,especi, varied ):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_TOTAL_PUBLICACIONES_OFERTADAS",[id_solicitud, especi,varied,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def Codex_Seleccion(id_solicitud, especie, variedad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CODEX_OFERTA', [id_solicitud, especie, variedad, salida])
    return salida.getvalue()













####-----------------------------------------------------------------------------------------------------------
def agregar_temporal_ofertar(v_des_especie, v_des_variedad, v_kilos, v_precio):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_TEMPORAL_OFERTA', [v_des_especie, v_des_variedad, v_kilos, v_precio, salida])
    return salida.getvalue()

def listar_temporal_ofertar():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_TEMPORAL_OFERTA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista