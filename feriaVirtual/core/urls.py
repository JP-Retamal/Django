from django.urls import path
from .views import *

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login/', login, name="login"),
   path('registro/', registro, name="registro"),
   path('registroExitoso/', redirecRegistro, name="registroExitoso"),
   path('detalle/<int:detalle_id>', detalle, name="detalle"),
   path('comprar/',comprar, name="comprar"),
   path('usuario/', usuario, name="detalle"),
   path('usuario/solicitud/', solicitud, name="solicitud"),
   path('usuario/pedido/', pedido, name="pedido"),
   path('usuario/informacion/', informacion, name="informacion")
]