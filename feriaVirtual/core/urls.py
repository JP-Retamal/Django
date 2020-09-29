from django.urls import path
from .views import home, login, registro, detalle, portalSaldos, crearSolicitud

# esta url en core se encarga de rutear las views

urlpatterns = [
    path('', home, name="home"),
    path('login/', login, name="login"),
    path('registro/', registro, name="registro"),
    path('detalle/<int:detalle_id>', detalle, name="detalle"),
    path('crearSolicitud', crearSolicitud, name="crearSolicitud"),
    path('portalSaldos/', portalSaldos, name="portalSaldos")
]
