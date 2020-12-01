from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User 
from django.contrib import messages
from django.db import connection
from django.contrib import auth
#-----------------------------------------
from .models import Usuario, pruebadetalle, Rol
#-----------------------------------------
from .metodos_views import *
from datetime import date
import cx_Oracle

from django.views.generic import TemplateView, View, DeleteView, CreateView
from django.core import serializers
from django.http import JsonResponse
import json
#--------Librerias PDF
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os
#------------------------------

# Create your views here. la funcion def home busca el template (controlador).
def ver(request):
   
    return render(request, 'grafico.html')


########################################            TODOS LOS USUARIOS         #################################################################
# ver pagina de inicio.
def home(request):
    #listar tarjetas de venta local.
    comprobar_usuarios()
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


# ACCESO USUARIOS AL SITEMA      
def login(request):
    # validar datos de usuarios.
    comprobar_usuarios()
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


def comprobar_usuarios():
    entry_list = list(Usuario.objects.all())
    for u in entry_list:
        if User.objects.filter(username=u.email):
            pass
            #print("usuario: "+ u.nombre+" está")
        else:
            #print("usuario: "+ u.nombre+" no existe")
            user = User.objects.create_user(username=u.email, first_name=u.nombre, last_name=u.ap_paterno, email=u.email, password=u.clave)
            if u.id_rol.pk == 1:
                user.is_staff = True
            else:
                user.is_staff = False
            user.groups.add(u.id_rol.pk)
            user.save()


# cerrar sesión de usuario.
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


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
           messages.success(request, '.')
    return  render(request, 'informacion.html', data) 


# vistas de usuario inicio general
def usuario(request):
    #usuario=request.GET['usuarioid']
    data = {
        'v_salida': contar_solicitudes_nuevas(),
        'v_vl_count': contar_ventas_locales(),
        'v_sol_publ': contar_solicitudes_publicadas(),
        'stock_nuevo': contar_stock_nuevo(),
        'resumen_vl': RESUMEN_VENTA_LOCAL(),
        'resumen_oc': RESUMEN_EXPORTACIONES(),
        'resumen_per': RESUMEN_PERDIDAS(),
        'resumen_stock': RESUMEN_STOCK_INICIAL(),
        'puntos': PUNTOS_ANIO(),
        'puntos_totales': PUNTOS_TOTALES(),
        'resumen_ventas_cerradas': RESUMEN_VENTAS_CERRADAS(),
        'resumen_totalvl': RESUMEN_TOTAL_VL(),
        'resumen_totaloc': EXPORTACIONES_TOTAL(),
        'perdidas_totales': PERDIDAS_TOTALES(),
        'TOTAL_STOCK':STOCK_INICIAL_TOTAL()

       
    }
 
    return render(request, 'usuario.html', data)

def dashboard_puntos(request):
    data = {
        'puntos': PUNTOS_ANIO()
    }
    return render(request, 'puntos.html', data)

def usuario_2(request):
    #usuario=request.GET['usuarioid']
    data = {
        'v_salida': contar_solicitudes_nuevas(),
       
    }
    return render(request, 'usuario_2.html', data)


##############################################          USUARIO COMERCIANTE        ############################################################
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


# usuario comerciante
@permission_required('core.add_pago')
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


# usuario comerciante
@permission_required('core.add_pago')
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
            messages.success(request, '.')
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


# usuario comerciante
@permission_required('core.add_pago')
def detalle_historial_compra(request):
    id=request.POST.get('idventa')
    email=request.POST.get('correo')
    variedad=request.POST.get('variedad')
    
    context = {
        'historial_hc': listar_detalle_historial_compra(id, email),
        'detalle_imagen':imagen_detalle(variedad)
    }
    
    return render(request, 'detalle_historial_compra.html', context)


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
            messages.error('Las contraseñas no coinciden')
        else:
            salidaR = validaRegistroRut(run_usuario)
            if salidaR ==1:
                messages.error('Problemas Datos existentes')
            else:
                if salidaR == 2:
                    salidaC = validaRegistroEmail(email)
                    if salidaC ==1:
                        messages.error('Problemas Datos existentes')
                    else:
                        if salidaC == 2:
                           #enc_clave = pbkdf2_sha256.encrypt(clave,roundlt_s=12000,sasize=32)
                           # clave = enc_clave
                            salida = agregar_comerciante(
                            run_usuario, nombre, ap_paterno, ap_materno, fecha_nac, email, direccion, celular, clave, comuna)
                            if salida == 1:
                                userDjango(email, nombre, ap_paterno, clave)
                                messages.success(request, '.')
                                return redirect("/") 
                            else:
                                messages.error('Error al guardar el registro')
                        else:
                            if salidaC == 3:
                                messages.error('Error al guardar el registro')
                else:
                    if salidaR == 3:
                        messages.error('Error al guardar el registro')
                        
    return render(request, 'registro.html', data)


##################################################         USUARIO PRODUCTOR              #####################################################

# LOS VEN PRODUCTOR Y ADMIN

def portalDeOfertas(request):
    data = {
        'bd_pedido': lista_pedido()
    }
   
    return render(request, 'portalDeOfertas.html', data)

# LOS VEN PRODUCTOR Y ADMIN

def detallePedido(request):
    id_Publicacion = request.GET.get('Publicacion')
    
    context = {
        'detallepedidos': listar_detallePedidos(id_Publicacion)
    }
    context['id_oferta']=id_Publicacion
    return render(request, 'detallePedido.html', context)


# USUARIO PRODUCTOR
@permission_required('core.add_detalleoferta')
def ofertaPruductor(request):
    id_Publicacion = request.GET.get('Publicacion')
    variedad = request.GET.get('variedad')
    context = {
        'bd_pedido': detalle_pedido_ofertar(id_Publicacion, variedad)
        
    }
    if request.method =="POST":
        especie          = request.POST.get('especie')
        variedad         = request.POST.get('variedad')
        kilos            = request.POST.get('kilos')
        precio           = request.POST.get('precio')
        fecha_cosecha    = request.POST.get('fecha')
        id_solicitud     = request.POST.get('solicitud')
        nombre_usuario   = request.POST.get('user')
        correo           = request.POST.get('correo')
      
        usuarioid        = SP_BUSCA_NUM_USUARIO(correo)

        especieid        = SP_BUSCA_NUM_especie(especie)

        salida           = OFERTA_PRODUCTOR(int(usuarioid))

        if salida == 1:
            print('Registro oferta productor Exitoso !!!')
            salida2 = OFERTA_PRODUCTOR_DETALLE(kilos, precio, fecha_cosecha, variedad, especieid, id_solicitud)
            if salida2 == 1:
                print('Registro oferta productor detalle Exitoso !!!')
                salida3 = OFERTA_PRODUCTOR_PUBLICACION(nombre_usuario, kilos, precio, fecha_cosecha, especie, usuarioid, variedad)
                if salida3 == 1:
                    print('Registro oferta productor publicación Exitoso !!!')
                    messages.success(request, ".")
                    return redirect("usuario/") 
                else:
                    print('fallo al insertar Registro oferta productor publicación :(')
            else:
                print('fallo al insertar Registro oferta detalle productor :(')
        else:
            print('fallo al insertar Registro oferta productor :(')

    return render(request, 'formulario_oferta.html',context)


# USUARIO PRODUCTOR (Modificado)
@permission_required('core.add_detalleoferta')
def historial_ofertas(request):
    info = request.POST.get("valcorreo")
    data = {
        'registros': listar_ofertas(info)
    }
    if request.method =="POST":
        if (request.POST.get("correo") != None):
            correo = request.POST.get("correo")
            print(correo)
            if (request.POST.get("publicacion") != None):
                idpubof = request.POST.get("publicacion")
                print(idpubof)
                data['registros']= listar_ofertas(correo)
                data['ver_repr1'] = ver_rp1(idpubof)
                pdf = render_to_pdf('include/pdf_template4.html', data)
                print(data['ver_repr1'])
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Informe de Compra N° %s.pdf" %(str(data['ver_repr1'][0][0]))
                #content = "attachment; filename=%s" %(filename)
                content = " filename=%s" %(filename) #para visualizar
                response['Content-Disposition'] = content
                return response



    return render(request, 'historial_ofertas.html', data)


# USUARIO PRODUCTOR
@permission_required('core.add_detalleoferta')
def datalle_historial_ofertas(request):
    id=request.POST.get('id')
    print(id)
    context = {
        'detalle_ho': listar_detalle_historial_oferta(id),
    }

    return render(request, 'detalle_historial_ofertas.html', context)

##################################################         USUARIO CLIENTE EXTERNO          ###################################################


# cliente externo
@permission_required('core.add_solicitud')
def variedad_por_especie(request):
    especie = request.GET.get('especie')
    data = {
        'variedad':listar_variedad(especie)
    }

    return render(request, 'variedad_por_especie.html', data)


# cliente externo
@permission_required('core.add_solicitud')
def solicitud(request):
    tituloPagina = 'Solicitudes'
    data = {
        'especie':listar_especie()
    }
    
    return render(request, 'solicitud.html', data)


# cliente externo
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
        externo = request.GET.get('usuariox',None)
        
        agregarSolicitud(fecha.strip(),externo.strip())

        user = {'id':obj.id,'especie':obj.especie,'variedad':obj.variedad,'cantidad':obj.cantidad}

        data = {
            'user': user
        }
        return JsonResponse(data)


# cliente externo


def agregarSolicitud(fecha_entrega, usuarioid):

    print(fecha_entrega)
    print(usuarioid)

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc('sp_ingresar_solicitud',[fecha_entrega, usuarioid])


# cliente externo
def listar_especie():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("sp_listar_especie",[out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)
    
    return lista


# cliente externo
def listar_variedad(especie):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("sp_listar_variedad",[out_cur, especie])

    lista=[]
    for fila in out_cur:
        lista.append(fila)
    
    return lista


@permission_required('core.add_solicitud')
def ordenes_externo(request):
    info = request.POST.get("valcorreo")
    #print(info)
    data = {
        'bd_orden': LISTAR_COSTOS_ORDEN(info),
        'orden_en_camino': LISTAR_ORDEN_EN_CAMINO(info),
        'orden_terminada': LISTAR_ORDEN_COMPLETADA(info)
    }
    if request.method =="POST":
        if (request.POST.get("IDS1") != None):
            PIDS1 = request.POST.get("IDS1")
            correo1 = request.POST.get("info1")
            data['bd_orden']=LISTAR_COSTOS_ORDEN(correo1)
            data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo1)
            data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo1)
            salida=verificar_cot(PIDS1)
            if salida ==1:
                data['ver_ordenp1'] = ver_oc1(PIDS1)
                data['ver_ordenp2'] = ver_oc2(PIDS1)
                
                pdf = render_to_pdf('include/pdf_template.html', data)
                print(salida)
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Cotizacion NÂ° %s.pdf" %(data['ver_ordenp1'][0][9])
                content = "attachment; filename=%s" %(filename)
                #content = " filename=%s" %(filename) #para visualizar
                response['Content-Disposition'] = content
                return response
        elif (request.POST.get("IDS2") != None):
            PIDS2 = request.POST.get("IDS2")
            correo2 = request.POST.get("info2")
            salida=verificar_cot(PIDS2)
            data['bd_orden']=LISTAR_COSTOS_ORDEN(correo2)
            data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo2)
            data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo2)
            if salida ==1:
                salida2 = aprobar_oc(PIDS2)
                if salida2 == 1:
                    messages.success(request, '.')
                    data['mensaje']="Orden de Compra Aprobada" 
                    data['bd_orden']=LISTAR_COSTOS_ORDEN(correo2)
                    data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo2)
                    data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo2)
                    return render(request, 'aceptar_ordenes.html', data)
            
        elif (request.POST.get("IDS3") != None):
            PIDS3 = request.POST.get("IDS3")
            correo3 = request.POST.get("info3")
            data['bd_orden']=LISTAR_COSTOS_ORDEN(correo3)
            data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo3)
            data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo3)
            salida=verificar_cot(PIDS3)
            if salida ==1:
                salida2 = rechazar_oc(PIDS3)
                if salida2 == 1:
                    messages.success(request, '.')
                    data['mensaje']="Orden de Compra Rechazada"
                    data['bd_orden']=LISTAR_COSTOS_ORDEN(correo3)
                    data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo3)
                    data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo3) 

        elif (request.POST.get("IDS4") != None):
            PIDS4 = request.POST.get("IDS4")
            correo4 = request.POST.get("info4")
            data['bd_orden']=LISTAR_COSTOS_ORDEN(correo4)
            data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo4)
            data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo4)
            salida = aceptar_oc_final(PIDS4)
            if salida == 1:
                messages.success(request, '.')
                data['mensaje']="Pedido Recepcionado"
                data['bd_orden']=LISTAR_COSTOS_ORDEN(correo4)
                data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo4)
                data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo4)
                
        elif (request.POST.get("IDS5") != None):
            PIDS5 = request.POST.get("IDS5")
            correo5 = request.POST.get("info5")
            data['bd_orden']=LISTAR_COSTOS_ORDEN(correo5)
            data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo5)
            data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo5)
            salida = rechazar_oc_final(PIDS5)
            if salida == 1: 
                messages.success(request, '.')       
                data['mensaje']="Pedido Rechazado"
                data['bd_orden']=LISTAR_COSTOS_ORDEN(correo5)
                data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correo5)
                data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correo5) 
        elif (request.POST.get("IDSX") != None):
            PIDSX = request.POST.get("IDSX")
            correoX = request.POST.get("infoX")
            data['bd_orden']=LISTAR_COSTOS_ORDEN(correoX)
            data['orden_en_camino']= LISTAR_ORDEN_EN_CAMINO(correoX)
            data['orden_terminada']= LISTAR_ORDEN_COMPLETADA(correoX)
            salida=verificar_cot(PIDSX)
            if salida ==2:
                data['ver_ordenp1'] = ver_oc1(PIDSX)
                data['ver_ordenp2'] = ver_oc2(PIDSX)
                pdf = render_to_pdf('include/pdf_template2.html', data)
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Orden de Compra NÂ° %s.pdf" %(data['ver_ordenp1'][0][0])
                content = "attachment; filename=%s" %(filename)
                #content = " filename=%s" %(filename) #para visualizar
                response['Content-Disposition'] = content
                return response
    return render(request, 'aceptar_ordenes.html', data)


@permission_required('core.add_solicitud')
def ordenes_externo_detalle(request):
    
    
    return render(request, 'ordenesExterno_detalle.html')


# cliente externo
@permission_required('core.add_solicitud')
def pedido(request):
    info = request.POST.get("valcorreo")
    print(info)
    data = {
        'bd_ex_pedido': listar_historial_solicitudes(info)
    }
    
    return render(request, 'pedido.html', data)


##################################################        USUARIO ADMINISTRADOR       #########################################################


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
                messages.success(request, '.')
                data['mensaje']="Solicitud Aprobada" 
                data['lista_solicitudes'] = listar_solicitudes()
        elif(request.POST.get('idsol2') != None):
            idsolR = request.POST.get('idsol2')
            salida2=rechazar_solicitud(idsolR)
            if salida2==1:
                data['mensaje']="Solicitud Rechazada"
                data['lista_solicitudes'] = listar_solicitudes()
    return render(request, 'solicitud-admin.html', data)


def detallesolicitudAdmin(request):
    info = request.POST.get("idsol")
    data = {
        'detalle_lista_solicitudes': listar_detalle_solicitudes(info)
    }
    print(data)
    return render(request, 'solicitud-detalle-admin.html', data)

def publicar_venta_local(request):
    data = {
        'saldos': LISTAR_SALDOS()
    }
    return render(request, 'saldos.html', data)


def detalle_publicar_vl(request):
    info = request.POST.get("idsol")
    data={
        'saldos_detalle': LISTAR_DETALLE_SALDOS(info)
    }

    return render(request, 'saldos_detalle.html', data)

def publicacion_vl(request):
    info = request.GET.get("idsol")
    idusuario = request.GET.get("usuario")
  
    data={
        'saldos_detalle': LISTAR_DETALLE_SALDOS(info),
        'bd_calidad': LISTAR_CALIDAD()
    }
    
    if request.method =="POST":
        precio       = request.POST.get('precio')
        descripcion  = request.POST.get('descripcion-venta')
        calidad      = request.POST.get('calidad')
        id_stock     = info
        usuarioid        = SP_BUSCA_NUM_USUARIO(idusuario)
        salida=AGREGAR_VENTA_LOCAL(usuarioid, precio, descripcion, calidad, id_stock)
        if salida == 1:
            print('Registro Exitoso !!!')
            messages.success(request, '.')
            return redirect("/") 
        else:
            print('Error al registrar los datos :(')

    return render(request, 'publicacion_saldo.html', data)

#------Informacion para pdf----
def render_pdf_view(request):
    template_path = 'user_printer.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

data = {
	"compañia": "BESTFRUIT",
	"nombre": "Gonzalo San Martin",
	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('include/pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('include/pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename=%s" %(filename)
		response['Content-Disposition'] = content
		return response

def revisar_publicaciones_pedidos(request):
    #listar_publicaciones_en_curso()
    context = {
        'lista_publicaciones': listar_publicaciones_of_activas()
        #'lista_publicaciones':listar_publicaciones_en_curso()
    }
    if request.method =="POST":
        if(request.POST.get('idsol') != None):
            idsox = request.POST.get("idsol")
            salida0 = generar_cot(idsox)
            if salida0 == 0:
                pass
            elif salida0 ==1:
                salida=verificar_cot(idsox)
                if salida==2:
                    pass
                elif salida==1:
                    context['ver_ordenp1'] = ver_oc1(idsox)
                    context['ver_ordenp2'] = ver_oc2(idsox)
                    pdf = render_to_pdf('include/pdf_template.html', context)
                    #return HttpResponse(pdf,content_type='application/pdf')
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Cotizacion N° %s.pdf" %(context['ver_ordenp1'][0][9])
                    content = "attachment; filename=%s" %(filename)
                    #content = " filename=%s" %(filename) #para visualizar
                    response['Content-Disposition'] = content
                    return response
    return render(request, 'revisar_publicacion_admin.html', context)


def revisar_detalle_pedido(request):
    idso = request.POST.get("idsol")
    espe = request.POST.get("espec")
    vari = request.POST.get("varie")
    variedad = vari.strip()
    
    context = {
        'lista_detalle_publicaciones': listar_detalle_publicaciones_of_activas(idso, espe, variedad),
        'lista_total_detalle_publicaciones': listar_total_publicaciones_of_activas(idso, espe, variedad)
    }
    print(context)
    return render(request, 'revisar_detalle_publicacion_admin.html',context)


def ventas_cerradas(request):
    context = {
        'lista_vcerradas': LISTAR_VENTAS_CERRADAS() 
    }
    #print(context)
    if request.method =="POST":
        if (request.POST.get("IDS2") != None):
            PIDS2 = request.POST.get("IDS2")
            correo2 = request.POST.get("info2")
            context['lista_vcerradas']= LISTAR_VENTAS_CERRADAS()
            context['ver_read1'] = ver_ra1(PIDS2)
            context['ver_read2'] = ver_ra2(PIDS2)
            context['pro_asociados'] = LISTAR_PRODUCTORES_ASOCIADOS(PIDS2)
            pdf = render_to_pdf('include/pdf_template3.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Reporte Ventas %s.pdf" %(str(context['ver_read1'][0][0]))
            #content = "attachment; filename=%s" %(filename) #para descargar
            content = " filename=%s" %(filename) #para visualizar
            response['Content-Disposition'] = content
            return response
    return render(request, 'ventas_terminadas.html', context)    


















def p_oferta(request):

    return render(request, 'ofertas_publicacion.html')