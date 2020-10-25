from django.contrib.auth.views import login_required
from django.urls import path, include
from .views import *

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login/', login, name="login"),
   path('logout/', logout, name="logout"),
   path('registro/', registro, name="registro"),
   path('detalle/', detalle, name="detalle"),
   path('comprar/', login_required(comprar), name="comprar"),
   path('usuario/', login_required(usuario), name="usuario"),
   path('usuario/solicitud/', login_required(solicitud), name="solicitud"),
   path('usuario/pedido/', login_required(pedido), name="pedido"),
   path('usuario/informacion/', login_required(informacion), name="informacion"),
   path('grafico/', ver, name="grafico"),
   path('usuario/historial_compra',login_required(historial_compra), name= "historial_compra"),
   path('usuario/detalle_historial_compra',login_required(detalle_historial_compra), name= "detalle_historial_compra"),
   
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

