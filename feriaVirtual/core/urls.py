from django.urls import path, include
from .views import *

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login/', login, name="login"),
   path('logout/', logout, name="logout"),
   path('registro/', registro, name="registro"),
   path('detalle/', detalle, name="detalle"),
   path('comprar/', comprar, name="comprar"),
   path('usuario/', usuario, name="usuario"),
   path('usuario/solicitud/', solicitud, name="solicitud"),
   path('usuario/pedido/', pedido, name="pedido"),
   path('usuario/informacion/', informacion, name="informacion"),
   path('grafico/', ver, name="grafico"),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

