from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib import auth
from django.template import Template, Context
from datetime import date
import cx_Oracle
from .metodos_views import *


# Create your views here. la funcion def home busca el template (controlador).
def ver(request):
   
    return render(request, 'grafico.html')

#ver pagina de inicio.
def home(request):
    #listar tarjetas de venta local.
    data = {
        'baja': listar_saldos_calidad_baja(),
        'media_alta': saldos_calidad_alta_media()
    }
    #enviar información de targeta a detalle.
    if request.method == 'POST':
        id_Publicacion = request.POST.get('Publicacion')
        context = {
            'db_vlocal': listar_detallesaldos(id_Publicacion)
        }
        return render(request,'detalle.html', context)
    else:   

        return render(request, 'index.html', data)

#vista detalle de venta local.
def detalle(request):
    #capturar informacón de detalle de tarjeta, renderizar y enviar selección de k a comprar.
    if request.method == 'GET':  
        kilos = request.GET.get('valorslider')
        context = {}
        context['kilos']=kilos
        return render(request, 'comprar.html"', context)
    else:
        return render(request, 'detalle.html')


#permiso de usuario
@permission_required('core.add_pago')
def comprar(request):
    #obtener valores y renderizar venta.
    id=request.GET['Publicacion']
    cant=request.GET['valorslider']
    context={
        'db_vlocal': listar_detallesaldos(id)
    }
    context['kilos']=cant
    #enviar información para registrar.
    if request.method == 'POST':
        descripcion  = request.POST.get('descripcion')
        monto        = request.POST.get('total')#number
        fecha_pago   = date.today()#date
        kilos        = request.POST.get('kilos')#number
        usuario      = request.POST.get('usuario')#varchar2
        especie      = request.POST.get('especie')#number
        variedad     = request.POST.get('variedad')#number
        idVentaLocal = request.POST.get('idVentaLocal')#numver
        idStock      = request.POST.get('idStock')#number
        salida = agregar_compra(descripcion, monto, fecha_pago, kilos, usuario, especie, variedad, idVentaLocal,  idStock)
        #si en exittosa o no, la compra se informa al usuario.
        if salida == 1:
            context['mensaje'] =  'Compra exitosa :) !!!'
            return redirect("/")              
        else:
            context['mensaje'] = 'Lo sentimos nose pudo efectuar la compra :( !!!'

    return render(request, 'comprar.html', context)


def login(request):
    #validar datos de usuarios.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            print('valido')
            # validación del usuario y estado de usuario.(activo)
            auth.login(request, user)
            # Redirecionar pagina de usuario.
            return HttpResponseRedirect("/usuario/")
        else:
            # ver errores y redireccionr.
            print('invalido')
            return HttpResponseRedirect("/login/")
 
    return render(request, 'login.html')


#cerrar sesión de usuario.
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


#Registro de usuario comerciante
def registro(request):
    #print(listar_regiones())
    data = {
        'region': listar_regiones()
    }

    if request.method == 'POST':
        
        if  request.POST.get('registro-pasaporte'):
            
            run_usuario  =   request.POST.get('registro-pass')
        else:
            run_usuario = request.POST.get('registro-rut')

        nombre      = request.POST.get('registro-nombre')
        ap_paterno  = request.POST.get('registro-Paterno')
        ap_materno  = request.POST.get('registro-materno')
        fecha_nac   = request.POST.get('registro-fecha')
        email       = request.POST.get('registro-correo')
        direccion   = request.POST.get('registro-direccion')
        celular     = request.POST.get('registro-celular')
        clave       = request.POST.get('registro-contrasenia1')
        clave2      = request.POST.get('registro-contrasenia2')
        comuna      = request.POST.get('registro-comuna')
        #validaciones de BD y enviar mensaje al usuario.
        if clave!=clave2:
            data['mensaje'] = 'Las contraseñas no coinciden'
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
                           #enc_clave = pbkdf2_sha256.encrypt(clave,rounds=12000,salt_size=32)
                           # clave = enc_clave
                            salida = agregar_comerciante(
                            run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna)
                            if salida == 1:
                                data['mensaje'] =  'Registro exitoso'
                                return redirect("/") 
                            else:
                                data['mensaje'] = 'Error al guardar el registro'
                        else:
                            if salidaC == 3:
                                data['mensaje'] = 'Error al guardar el registro'
                else:
                    if salidaR == 3:
                        data['mensaje'] = 'Error al guardar el registro'
                        
    return render(request, 'registro.html', data)


# vistas de usuario
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