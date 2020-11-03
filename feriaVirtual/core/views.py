from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from django.contrib import auth
#-----------------------------------------
from .models import Usuario, pruebadetalle
#-----------------------------------------
from .metodos_views import *
from datetime import date
import cx_Oracle

from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
import json
#------------------------------

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
        id_Publicacion = request.POST.get('Publicacion')
        context = {
            'db_vlocal': listar_detallesaldos(id_Publicacion)
        }
        context['kilos']=cant
        return render(request,'transbank.html', context)

    return render(request, 'comprar.html', context)

def transbank(request):
   
    id=request.POST.get['Publicacion']
    cant=request.POST.get['valorslider']
    context={
        'db_vlocal': listar_detallesaldos(id)
    }
    context['kilos']=cant
    #enviar información para registrar.
    if request.method == 'GET':
        id_Publicacion = request.POST.get('Publicacion')
        context = {
            'db_vlocal': listar_detallesaldos(id_Publicacion)
        }
        context['kilos']=cant
        return render(request,'redcompra.html', context)
  
    return render(request, 'transbank.html', context)

def medioPago(request):
    #obtener valores y renderizar venta.
    id=request.GET['Publicacion']
    cant=request.GET['kilos']
    context={
        'db_vlocal': listar_detallesaldos(id)
    }
    context['kilos']=cant
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
            context['mensaje'] = 'compra exitosa!!!'
            return redirect("/")              
        else:
            context['mensaje'] = 'Lo sentimos nose pudo efectuar la compra :( !!!'
    return render(request, 'redcompra.html',context)

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
    context['id_oferta']=id_Publicacion
    return render(request, 'detallePedido.html', context)

def ofertaPruductor(request):
    id_Publicacion = request.GET.get('Publicacion')
    context = {
        'detallepedidos': listar_detallePedidos(id_Publicacion)
    }
    return render(request, 'formulario_oferta.html',context)



def historial_ofertas(request):
    info = request.POST.get("valcorreo")
    print(info)
    data = {
        'registros': listar_ofertas(info)
    }

    return render(request, 'historial_ofertas.html', data)

def datalle_historial_ofertas(request):
    id=request.POST.get('id')
    print(id)
    context = {
        'detalle_ho': listar_detalle_historial_oferta(id),
    }

    return render(request, 'detalle_historial_ofertas.html', context)

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#COPIAR DESDE AQUI

def variedad_por_especie(request):
    especie = request.GET.get('especie')
    data = {
        'variedad':listar_variedad(especie)
    }

    return render(request, 'variedad_por_especie.html', data)


def solicitud(request):
    tituloPagina = 'Solicitudes'
    data = {
        'especie':listar_especie(),
    }    
    return render(request, 'solicitud.html', data)


class CreateCrudUser(View):
    def  get(self, request):

        name1 = request.GET.get('especie', None)
        address1 = request.GET.get('variedad', None)
        age1 = request.GET.get('cantidad', None)
        print(name1)
        print(address1)
        agregarfruta(name1.strip(),address1.strip(),age1.strip())



        user = {'id':obj.id,'especie':obj.especie,'variedad':obj.variedad,'cantidad':obj.cantidad}

        data = {
            'user': user
        }
        return JsonResponse(data)

class CreateCrudUser2(View):
    def  get(self, request):

        fecha = request.GET.get('fecha', None)

        print(fecha)
        agregarSolicitud(fecha)

        

        user = {'id':obj.id,'especie':obj.especie,'variedad':obj.variedad,'cantidad':obj.cantidad}

        data = {
            'user': user
        }
        return JsonResponse(data)

def agregarfruta(especie,variedad,cantidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc('sp_agregar_prueba',[especie,variedad,cantidad])
    

def listar_especie():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("sp_listar_especie",[out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)
    
    return lista

def listar_variedad(especie):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("sp_listar_variedad",[out_cur, especie])

    lista=[]
    for fila in out_cur:
        lista.append(fila)
    
    return lista


def agregarSolicitud(fecha):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc('sp_ingresar_solicitud',[fecha])


#HASTA AQUII

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
    data = {
        'lista_solicitudes': listar_solicitudes()
    }
    if request.method =="POST":
        if(request.POST.get('idsol1') != None):
            idsolA = request.POST.get('idsol1')
            salida1=aprobar_solicitud(idsolA)
            if salida1==1:

                data['mensaje']="Solicitud Aprobada" 
                data['lista_solicitudes'] = listar_solicitudes()
        elif(request.POST.get('idsol2') != None):
            idsolR = request.POST.get('idsol2')
            salida2=rechazar_solicitud(idsolR)
            if salida2==1:
                data['mensaje']="Solicitud Rechazada"
                data['lista_solicitudes'] = listar_solicitudes()
    return render(request, 'solicitud-admin.html', data)

#---------------------------------------------------------------------------

def detallesolicitudAdmin(request):
    info = request.POST.get("idsol")
    data = {
        'detalle_lista_solicitudes': listar_detalle_solicitudes(info)
    }
    print(data)
    return render(request, 'solicitud-detalle-admin.html', data)

def p_oferta(request):

    return render(request, 'ofertas_publicacion.html')