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
   path('transbank',login_required(transbank), name='transbank'),
   path('medioPago', login_required(medioPago), name="medioPago"),
   path('usuario/', login_required(usuario), name="usuario"),
   path('usuario/pedido', login_required(pedido), name="pedido"),
   path('usuario/informacion', login_required(informacion), name="informacion"),
   path('administracion/', login_required(homeAdmin), name="homeAdmin"),
   path('administracion/solicitud', login_required(solicitudAdmin), name="solicitudAdmin"),
   path('administracion/solicitud_detalle', login_required(detallesolicitudAdmin), name="detallesolicitudAdmin"),
   path('portalDeOfertas', login_required(portalDeOfertas), name="portalDeOfertas"),
   path('detallePedido', login_required(detallePedido), name="detallePedido"),
   path('usuario/historial_compra',login_required(historial_compra), name= "historial_compra"),
   path('usuario/detalle_historial_compra',login_required(detalle_historial_compra), name= "detalle_historial_compra"),
   path('usuario/historial_ofertas', login_required(historial_ofertas), name="historial_ofertas"),
   path('usuario/detalle_hitorial_ofertas', login_required(datalle_historial_ofertas), name="detalle_historial_ofertas"),
   path('oferta_productor', login_required(ofertaPruductor), name="oferta_productor"),
   path('usuario/ordenes', ordenes_externo, name="ordenesExterno"),
   path('usuario/ordenes_detalle', ordenes_externo_detalle, name="ordenExterno_detalle"),
   path('variedades',login_required(variedad_por_especie), name="variedades"),
   path('usuario/solicitud', login_required(solicitud), name="solicitud"),
   path('ajax/crud/create/', login_required(CreateCrudUser.as_view()), name='crud_ajax_create'),
   path('ajax/crud/create_2/',login_required(CreateCrudUser2.as_view()), name='crud_ajax_create2'),
   path('administracion/publicaciones_ofertadas', login_required(revisar_publicaciones_pedidos), name="revisar_publicaciones_pedidos"),
   path('administracion/detalle_publicacion_ofertada', login_required(revisar_detalle_pedido), name="revisar_detalle_pedido"),



#-------------------------------------------------------------------------------
   path('variedad/', variedad_por_especie, name="variedad"),
   path('p_oferta', p_oferta, name='p_oferta'),
   path('grafico/', ver, name="grafico"),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

