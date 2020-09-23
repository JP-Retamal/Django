from django.shortcuts import render

# Create your views here. la funcion def home busca el template (controlador)

def home(request):

    return render(request, 'index.html')

def login(request):

    return render(request, 'login.html')

def registro(request):
    fechaActual = '22/09/2020'
    return render(request, 'registro.html', { 'fechaActual' : fechaActual })