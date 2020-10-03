from django.urls import path
from .views import home, login, registro, detalle, usuario, solicitud

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login/', login, name="login"),
   path('registro/', registro, name="registro"),
   path('detalle/', detalle, name="detalle"),
   path('usuario/', usuario, name="detalle"),
   path('usuario/solicitud/', solicitud, name="solicitud")
]