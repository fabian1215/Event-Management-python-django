from django.urls import path
from . import views

app_name = 'interoperabilidad'

urlpatterns = [
    path('api/eventos', views.eventos_json, name='eventos_json'),
    path('listar-proveedor-eventos', views.ProveedorEventosListar.as_view(), name='proveedor_eventos_listar'),
    path('listar-proveedor-eventos/<int:pk>', views.ProveedorEventosDetalle.as_view(), name='proveedor_eventos_detalle'),
    path('crear-proveedor-eventos', views.ProveedorEventosCrear.as_view(), name='proveedor_eventos_crear'),
    path('actualizar-proveedor-eventos/<int:pk>', views.ProveedorEventosActualizar.as_view(), name='proveedor_eventos_actualizar'),
    path('eliminar-proveedor-eventos/<int:pk>', views.ProveedorEventosEliminar.as_view(), name='proveedor_eventos_eliminar'),
]