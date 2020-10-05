from django.shortcuts import render
from datetime import date
import cx_Oracle
from .metodos_views import *
import base64
# Create your views here. la funcion def home busca el template (controlador)

def home(request):
    #print(listar_saldos_calidad_baja())
    data = {
        'baja': listar_saldos_calidad_baja(),
        'media_alta': saldos_calidad_alta_media()
    }
    
    return render(request, 'index.html', data)

def login(request):
    tituloPagina = 'Ingreso'
    return render(request, 'login.html', { 'tituloPagina' : tituloPagina })

def registro(request):
    tituloPagina = 'Registro'
    fechaActual = date.today()
    return render(request, 'registro.html', { 'fechaActual' : fechaActual, 'tituloPagina' : tituloPagina })

def detalle(request, detalle_id):
    # print(listar_detallesaldos(detalle_id))
    data = {
        'db_vlocal': listar_detallesaldos(detalle_id)
    }
    return render(request, 'detalle.html', data)

def usuario(request):
    tituloPagina = 'Perfil'
    nombreUsuario = 'Jesus'
    return render(request, 'usuario.html', { 'tituloPagina' : tituloPagina, 'nombreUsuario' : nombreUsuario})

def solicitud(request):
    tituloPagina = 'Solicitudes'
    return render(request, 'solicitud.html', { 'tituloPagina' : tituloPagina})

def pedido(request):
    tituloPagina = 'Pedidos'
    return render(request, 'pedido.html', { 'tituloPagina' : tituloPagina})

def informacion(request):
    tituloPagina = 'Informacion'
    return render(request, 'informacion.html', { 'tituloPagina' : tituloPagina})