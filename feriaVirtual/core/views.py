from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib import messages
from django.db import connection
from django.contrib import auth
from .models import Usuario
from .metodos_views import *
from datetime import date
import cx_Oracle



# Create your views here. la funcion def home busca el template (controlador).
def ver(request):
   
    return render(request, 'grafico.html')

# ver pagina de inicio.
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

# vista detalle de venta local.
def detalle(request):
    #capturar informacón de detalle de tarjeta, renderizar y enviar selección de k a comprar.
    if request.method == 'GET':  
        kilos = request.GET.get('valorslider')
        context = {}
        context['kilos']=kilos
        return render(request, 'comprar.html"', context)
    else:
        return render(request, 'detalle.html')


# usuario comerciante
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


# usuario comerciante
@permission_required('core.add_pago')
def historial_compra(request):
    info = request.POST.get("valcorreo")
    print(info)
    data = {
        'registros': listar_historial_compra(info)
    }

    return render(request, 'historial_compra.html', data)


@permission_required('core.add_pago')
def detalle_historial_compra(request):
    id=request.POST.get('idventa')
    print(id)
    context = {
        'historial_hc': listar_detalle_historial_compra(id),
    }
        
    return render(request, 'detalle_historial_compra.html', context)

#--------------------------------------------------------------------------------------------

def login(request):
    # validar datos de usuarios.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None and user.is_active:   
            # validación del usuario y estado de usuario.(activo)
            auth.login(request, user)
        else:
            # ver errores y redireccionr.
            
            return HttpResponseRedirect("/login")
 
    return render(request, 'login.html')


# cerrar sesión de usuario.
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


# Registro de usuario comerciante
def registro(request):
    #print(listar_regiones())
    data = {
        'region': listar_regiones()
    }

    if request.method == 'POST':
        
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
                                userDjango(email, nombre, ap_paterno, clave)
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

# actualizar datos cuenta
def informacion(request):
    info = request.GET.get("valcorreo")
    data = {
        'usuario': buscar_usuario(info),
        'region': listar_regiones()
    }
    if request.method =="POST":
        celular = request.POST.get('informacion-telefono')
        direccion   = request.POST.get('informacion-direccion')
        id_comuna     = request.POST.get('comuna')
        salida=modificar_usuario( info, celular, direccion, id_comuna)
        if salida==1:
           data['mensaje']="Datos actualizados" 
           data['usuario']=buscar_usuario(info)
    return  render(request, 'informacion.html', data) 

#--------------------------------------------------------------------------

# vistas de usuario inicio general
def usuario(request):
    tituloPagina = 'Perfil'
    nombreUsuario = 'Jesus'
    return render(request, 'usuario.html', { 'tituloPagina' : tituloPagina, 'nombreUsuario' : nombreUsuario})


#-------------------------------------------------------------------------

# usuario productor
def portalDeOfertas(request):
    data = {
        'bd_pedido': lista_pedido()
    }
   
    return render(request, 'portalDeOfertas.html', data)


def detallePedido(request):
    id_Publicacion = request.GET.get('Publicacion')
    context = {
        'detallepedidos': listar_detallePedidos(id_Publicacion)
    }
        
    return render(request, 'detallePedido.html', context)

def ofertaPruductor(request):

    return render(request, 'formulario_oferta.html')

def historial_ofertas(request):
    info = request.POST.get("valcorreo")
    print(info)
    data = {
        'registros': listar_ofertas(info)
    }

    return render(request, 'historial_ofertas.html', data)

def datalle_historial_ofertas(request):
    id=request.POST.get('idventa')
    print(id)
    context = {
        'detalle_ho': listar_detalle_historial_oferta(id),
    }

    return render(request, 'detalle_historial_ofertas.html', context)

#--------------------------------------------------------------------------------------
#COPIAR DESDE AQUI
# Usuario externo.
def variedad_por_especie(request):
    especie = request.GET.get('especie')
    data = {
        'variedadEspecie':listar_subcategorias_por_categoria(especie)
    }

    return render(request, 'variedades.html', data)



def solicitud(request):
   
    data = {
        'especie':listar_especie(),
    }    

    return render(request, 'solicitud.html', data)



#----------------------------------------------------------------------------------

def pedido(request):
    tituloPagina = 'Pedidos'
    return render(request, 'pedido.html', { 'tituloPagina' : tituloPagina})


@permission_required('core.view_ventalocal')
def homeAdmin(request):
    tituloPagina = 'Administracion'
    return render(request, 'base-admin.html', { 'tituloPagina' : tituloPagina})


@permission_required('core.view_ventalocal')
def solicitudAdmin(request):
    tituloPagina = 'Solicitudes'
    return render(request, 'solicitud-admin.html', { 'tituloPagina' : tituloPagina})

#---------------------------------------------------------------------------

def publicacion_solicitud(request):

    return render(request, 'publicacion_admin.html')
