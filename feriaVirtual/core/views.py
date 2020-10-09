from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from passlib.hash import pbkdf2_sha256
from datetime import date
import cx_Oracle
from .metodos_views import *

# Create your views here. la funcion def home busca el template (controlador)

def home(request):
    
    data = {
        'baja': listar_saldos_calidad_baja(),
        'media_alta': saldos_calidad_alta_media()
    }
    
    return render(request, 'index.html', data)

def login(request):
    tituloPagina = 'Ingreso'
    return render(request, 'login.html', { 'tituloPagina' : tituloPagina })

def registro(request):
    print(listar_regiones())
    data = {
        'region': listar_regiones()
    }

    if request.method == 'POST':
        run_usuario = request.POST.get('registro-rut')
        #pasaporte = request.POST.get('registro-pasaporte')
        nombre = request.POST.get('registro-nombre')
        ap_paterno = request.POST.get('registro-Paterno')
        ap_materno = request.POST.get('registro-materno')
        fecha_nac = request.POST.get('registro-fecha')
        email = request.POST.get('registro-correo')
        direccion = request.POST.get('registro-direccion')
        celular = request.POST.get('registro-celular')
        clave = request.POST.get('registro-contrasenia1')
        clave2 = request.POST.get('registro-contrasenia2')
        comuna = request.POST.get('registro-comuna')

        if clave!=clave2:
            data['mensaje2'] = 'Las contraseñas no coinciden'
        else:
            salidaR = validaRegistroRut(run_usuario)
            if salidaR ==1:
                data['mensaje'] = 'El rut ingresasdo ya existe'
            else:
                if salidaR == 2:
                    salidaC = validaRegistroEmail(email)
                    if salidaC ==1:
                        data['mensaje'] = 'El email ingresasdo ya existe'
                    else:
                        if salidaC == 2:
                            enc_clave = pbkdf2_sha256.encrypt(clave,rounds=12000,salt_size=32)
                            clave = enc_clave
                            salida = agregar_comerciante(
                            run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna)
                            if salida == 1:
                                #return redirect("login")
                                return render(request, 'redirecRegistro.html')
                            else:
                                data['mensaje'] = 'Error al guardar el registro'
                        else:
                            if salidaC == 3:
                                data['mensaje'] = 'Error al guardar el registro'
                else:
                    if salidaR == 3:
                        data['mensaje'] = 'Error al guardar el registro'
                        
    return render(request, 'registro.html', data)

def detalle(request, detalle_id):
    
    data = {
        'db_vlocal': listar_detallesaldos(detalle_id)
    }
    return render(request, 'detalle.html', data)


def comprar(request):

    return render(request, 'comprar.html')

def redirecRegistro(request):
    tituloPagina = 'Registro Exitoso'
    return render(request, 'redirecRegistro.html', { 'tituloPagina' : tituloPagina })






    

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