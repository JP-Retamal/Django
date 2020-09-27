from django.urls import path
from .views import home, login, registro, detalle, portalSaldos

#esta url en core se encarga de rutear las views

urlpatterns = [
   path('', home, name="home"),
   path('login/', login, name="login"),
   path('registro/', registro, name="registro"),
   path('detalle/<int:detalle_id>', detalle, name="detalle"),
   path('portalSaldos/', portalSaldos, name="portalSaldos")
]