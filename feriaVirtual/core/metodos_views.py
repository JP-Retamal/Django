from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime
from datetime import date
import cx_Oracle
import base64


########################################            TODOS LOS USUARIOS         #################################################################

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

##############################################          USUARIO COMERCIANTE        ############################################################

# METODOS PARA AGREGAR UN COMERCIANTE EN PAGINA DE REGISTRO
def agregar_comerciante(run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_COMERCIANTE', [run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna, salida])
    return salida.getvalue()

# METODO PARA REALIZAR COMPRA DE PROMOCIÓN
def agregar_compra(descripcion, monto, fecha_pago, kilos, usuario, especie, variedad, idVentaLocal,  idStock):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PAGO', [descripcion, monto, fecha_pago, kilos, usuario, especie, variedad, idVentaLocal,  idStock, salida])
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

def listar_historial_compra(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_HISTORIAL_COMPRA", [correo,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listar_detalle_historial_compra(id_venta, correo):
    django_cursor = connection.cursor()
    cursor        = django_cursor.connection.cursor()
    out_cur       = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_DETALLE_HISTORIAL_COMPRA", [id_venta, correo, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def imagen_detalle(variedad):
    django_cursor = connection.cursor()
    cursor        = django_cursor.connection.cursor()
    out_cur       = django_cursor.connection.cursor()

    cursor.callproc("SP_DETALLE_HISTORIAL_COMPRA_IMAGEN", [variedad, out_cur])

    lista2 = []  
    for fila in out_cur:
        data = {
            'imagen':str(base64.b64encode(fila[0].read()), 'utf-8')
        }

        lista2.append(data)

    return lista2

def userDjango(email, nombre, ap_paterno, clave):
    user = User.objects.create_user(username=email, first_name=nombre, last_name=ap_paterno, email=email, password=clave)
    user.is_staff = False
    user.groups.add(2)
    user.save()


def admin(user):
    return user.is_authenticated() and user.has_perm("view_ventalocal")

def PUNTOS_ANIO():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_PUNTOS_ANIO",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def PUNTOS_TOTALES():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_PUNTOS_TOTALES",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def lista_puntosMarzo():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_PUNTOS_MARZO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
##################################################          USUARIO PRODUCTOR            #####################################################


# METODOS PARA ACCEDER AL SISTEMA EN LOGIN DE USUARIO COMERCIANTE

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


def OFERTA_PRODUCTOR(usuarioid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_OFERTA_PRODUCTOR', [usuarioid, salida])
    return salida.getvalue()


def OFERTA_PRODUCTOR_DETALLE(kilos, precio, fecha_cosecha, variedad, especieid, id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_OFERTA_PRODUCTOR_DETALLE', [kilos, precio, fecha_cosecha, variedad, especieid, id_solicitud, salida])
    return salida.getvalue()


def OFERTA_PRODUCTOR_PUBLICACION(nombre_usuario, kilo, precio, fecha_cosecha, especie, usuarioid, variedad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_OFERTA_PRODUCTOR_PUBLICACION', [nombre_usuario, kilo, precio, fecha_cosecha, especie, usuarioid, variedad, salida])
    return salida.getvalue()


def SP_BUSCA_NUM_USUARIO(correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_BUSCA_NUM_USUARIO",[correo, salida])
    return salida.getvalue()


def SP_BUSCA_NUM_especie(especie):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_BUSCA_NUM_especie",[especie, salida])
    return salida.getvalue()


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

##################################################         USUARIO CLIENTE EXTERNO          ###################################################


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


def listar_historial_solicitudes(email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_EX_PEDIDO",[email, out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def LISTAR_COSTOS_ORDEN(email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_COSTOS_ORDEN",[email, out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def contar_ordencompra_nuevas(usuariois):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_CONTAR_ORDENCOMPRA_NUEVAS", [usuarioid, out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

#LISTAS ORDEN DE COMPRA----------------------------------------
def LISTAR_COSTOS_ORDEN(email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_COSTOS_ORDEN",[email, out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def LISTAR_ORDEN_EN_CAMINO(email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_ORDEN_EN_CAMINO",[email, out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def LISTAR_ORDEN_COMPLETADA(email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_ORDEN_TERMINADA",[email, out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

##################################################        USUARIO ADMINISTRADOR       #########################################################

def contar_solicitudes_nuevas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_CONTAR_SOLICITUDES_NUEVAS", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def contar_ventas_locales():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_CONTAR_VENTAS_LOCALES", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def contar_solicitudes_publicadas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_CONTAR_SOLICITUDES_PUBLICADAS", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def contar_stock_nuevo():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_CONTAR_STOCK_SALDO_NUEVO", [out_cur])
    
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


def listar_publicaciones_of_activas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_PUBLICACIONES_OFERTADAS",[out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[9].read()), 'utf-8')
        }
        lista.append(data)
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

def ver_oc1(ids):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_VER_COTIZACION1",[ids,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def ver_oc2(ids):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_VER_COTIZACION2",[ids,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def generar_cot(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_GENERAR_COTIZACION', [id_solicitud, salida])
    return salida.getvalue()

def verificar_cot(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_VERIFICAR_COTIZACION', [id_solicitud, salida])
    return salida.getvalue()

def aprobar_oc(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACEPTAR_OC', [id_solicitud, salida])
    return salida.getvalue()

def rechazar_oc(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_RECHAZAR_OC', [id_solicitud, salida])
    return salida.getvalue()

def aceptar_oc_final(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CONFIRMAR_LLEGADA_OC', [id_solicitud, salida])
    return salida.getvalue()

def rechazar_oc_final(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_RECHAZAR_LLEGADA_OC', [id_solicitud, salida])
    return salida.getvalue()

####################### ver ##########################
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

##################################################        USUARIO ADMINISTRADOR       #########################

def RESUMEN_VENTA_LOCAL():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_RESUMEN_VENTA_LOCAL",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def RESUMEN_EXPORTACIONES():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_RESUMEN_EXPORTACIONES",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def RESUMEN_PERDIDAS():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_RESUMEN_PERDIDAS",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def RESUMEN_STOCK_INICIAL():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_RESUMEN_STOCK_INICIAL",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista




def LISTAR_SALDOS():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_SALDOS", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def LISTAR_DETALLE_SALDOS(STOCK_ID):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SALDOS_DETALLE",[STOCK_ID, out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def LISTAR_VARIEDAD():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_VARIEDAD", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def LISTAR_CALIDAD():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_CALIDAD", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def AGREGAR_VENTA_LOCAL(v_id_usuario, v_precio, v_descripcion, v_id_calidad, v_id_stock):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_VENTA_LOCAL', [v_id_usuario, v_precio, v_descripcion, v_id_calidad, v_id_stock, salida])
    return salida.getvalue()

def RESUMEN_VENTAS_CERRADAS():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_RESUMEN_VENTAS_TERMINADAS",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def LISTAR_VENTAS_CERRADAS():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_VENTAS_TERMINADAS",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def ver_ra1(ids):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_VER_REPORTE_ADMIN1",[ids,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def ver_ra2(ids):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_VER_REPORTE_ADMIN2",[ids,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def LISTAR_PRODUCTORES_ASOCIADOS(id_solicitud):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTORES_ASOCIADOS",[id_solicitud,out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


#------ Reporte Productor
def ver_rp1(ids):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_VER_REPORTE_PRODUCTOR",[ids,out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def RESUMEN_TOTAL_VL():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_RESUMEN_TOTAL_VL",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def EXPORTACIONES_TOTAL():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_EXPORTACIONES_TOTAL",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista



def PERDIDAS_TOTALES():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_PERDIDAS_TOTALES",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def STOCK_INICIAL_TOTAL():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_STOCK_INICIAL_TOTAL",[out_cur])
   
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista