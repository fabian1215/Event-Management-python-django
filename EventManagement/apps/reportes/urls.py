from django.urls import path

from apps.reportes.views import *

app_name = 'reportes'

urlpatterns = [
    path('ver-facturas-eventos', ver_facturas_eventos, name='ver-facturas-eventos'),
    path('ver-facturas-evento/<int:evento_id>', ver_facturas_evento, name='ver-facturas-evento'),
    path('dinero-por-evento', vista_dinero_por_evento, name="dinero-por-evento"),
    path('dinero_por_evento_json', dinero_por_evento_json, name="dinero_por_evento_json"),
    path('boletas-por-evento', vista_boletas_por_evento, name="boletas-por-evento"),
    path('boletas_por_evento_json', boletas_por_evento_json, name="boletas_por_evento_json"),
]