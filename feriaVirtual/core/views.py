from django.shortcuts import render
from django.db import connection
from datetime import date
# Create your views here. la funcion def home busca el template (controlador)

def home(request):
    tituloPagina = 'Inicio'
    return render(request, 'index.html', { 'tituloPagina' : tituloPagina })

def login(request):
    tituloPagina = 'Ingreso'
    return render(request, 'login.html', { 'tituloPagina' : tituloPagina })

def registro(request):
    tituloPagina = 'Registro'
    fechaActual = date.today()
    print(listar_por_regiones())#ver listado en consola
    data = {
        'regiones':listar_por_regiones()
    }
    return render(request, 'registro.html', { 'fechaActual' : fechaActual, 'tituloPagina' : tituloPagina , 'data':data})

def detalle(request):#detalle_id
   # print(listar_detallesaldos(detalle_id))
    tituloPagina = 'Manzana Candy'
    precio = '{:,}'.format(1990).replace(',','.')
    cantidad = '1'
    return render(request, 'detalle.html', { 'tituloPagina' : tituloPagina, 'precio' : precio, 'cantidad' : cantidad })

def portalSaldos(request):
    print(listar_saldos())#ver listado en consola
    data = {
        'saldos':listar_saldos()
    }
    return render(request, 'portalSaldos.html', data)

# METODOS PARA ACCEDER A DATOS DEL PLSQL

def listar_saldos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SALDOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def listar_por_regiones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_POR_REGIONES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
def listar_detallesaldos(detalle_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_BUSCAR_DETALLE_VLOCAL", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista  