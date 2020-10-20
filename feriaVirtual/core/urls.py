from django.urls import path
from .views import *

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login/', login, name="login"),
   path('registro/', registro, name="registro"),
   path('detalle/', detalle, name="detalle"),
   path('comprar/', comprar, name="comprar"),
   path('usuario/', usuario, name="usuario"),
   path('usuario/solicitud/', solicitud, name="solicitud"),
   path('usuario/pedido/', pedido, name="pedido"),
   path('usuario/informacion/', informacion, name="informacion"),
   path('grafico/', ver, name="grafico"),
   path('detalle2/', detalle2),
]