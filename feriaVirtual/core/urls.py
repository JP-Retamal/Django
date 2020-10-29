from django.contrib.auth.views import login_required
from django.urls import path, include
from .views import *

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login', login, name="login"),
   path('logout/', logout, name="logout"),
   path('registro', registro, name="registro"),
   path('detalle/', detalle, name="detalle"),
   path('comprar/', login_required(comprar), name="comprar"),
   path('usuario/', login_required(usuario), name="usuario"),
   path('usuario/solicitud', login_required(solicitud), name="solicitud"),
   path('usuario/pedido', login_required(pedido), name="pedido"),
   path('usuario/informacion', login_required(informacion), name="informacion"),
   path('administracion/', homeAdmin, name="homeAdmin"),
   path('administracion/solicitud', login_required(solicitudAdmin), name="solicitudAdmin"),
   path('portalDeOfertas', login_required(portalDeOfertas), name="portalDeOfertas"),
   path('detallePedido', login_required(detallePedido), name="detallePedido"),
   path('usuario/historial_compra',login_required(historial_compra), name= "historial_compra"),
   path('usuario/detalle_historial_compra',login_required(detalle_historial_compra), name= "detalle_historial_compra"),
   path('usuario/historial_ofertas', login_required(historial_ofertas), name="historial_ofertas"),
   path('usuario/detalle_hitorial_ofertas', login_required(datalle_historial_ofertas), name="detalle_historial_ofertas"),
   path('oferta_productor', ofertaPruductor, name="oferta_productor"),
   path('usuario/publicacion_solicitud', publicacion_solicitud, name="publicacion_solicitud"),
   path('grafico/', ver, name="grafico"),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

