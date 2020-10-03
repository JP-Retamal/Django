from django.shortcuts import render
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
    return render(request, 'registro.html', { 'fechaActual' : fechaActual, 'tituloPagina' : tituloPagina })

def detalle(request):
    tituloPagina = 'Manzana Candy'
    precio = '{:,}'.format(1990).replace(',','.')
    cantidad = '1'
    return render(request, 'detalle.html', { 'tituloPagina' : tituloPagina, 'precio' : precio, 'cantidad' : cantidad })

def usuario(request):
    tituloPagina = 'Perfil'
    nombreUsuario = 'Jesus'
    return render(request, 'usuario.html', { 'tituloPagina' : tituloPagina, 'nombreUsuario' : nombreUsuario})

def solicitud(request):
    tituloPagina = 'Solicitudes'
    return render(request, 'solicitud.html', { 'tituloPagina' : tituloPagina})