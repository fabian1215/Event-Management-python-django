from django.urls import path

from apps.compras.views import *

app_name = 'compras'

urlpatterns = [
    path('ver-factura/<int:id_factura>', ver_factura, name='ver-factura'),
    path('carrito-compras', carrito_compras, name='carrito-compras'),
    path('mis-compras', mis_compras, name='mis-compras'),
    path('eliminar-elemento-carrito/<int:elemento_id>', eliminar_elemento_carrito, name='eliminar-elemento-carrito'),
    path('agregar-boletas-evento-carrito/<int:id_evento>', agregar_boletas_evento_carrito, name='agregar-boletas-evento-carrito'),
]