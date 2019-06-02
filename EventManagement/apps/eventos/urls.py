from django.urls import path

from apps.eventos.views import *

app_name = 'eventos'

urlpatterns = [
    path('gestionar-evento/<int:evento_id>', gestionar_evento, name='gestionar-evento'),
    path('gestionar-tipo-eventos', gestionar_tipo_eventos, name='gestionar-tipo-eventos'),
    path('gestionar-tipo-evento/<int:tipo_evento_id>', gestionar_tipo_evento, name='gestionar-tipo-evento'),
    path('gestionar-categorias-evento/<int:evento_id>', gestionar_categorias_evento, name='gestionar-categorias-evento'),
    path('gestionar-categorias-tipo-evento/<int:tipo_evento_id>', gestionar_categorias_tipo_evento, name='gestionar-categorias-tipo-evento'),
    path('gestionar-eventos', gestionar_eventos, name='gestionar-eventos'),
    path('catalogo-eventos', catalogo_eventos, name='catalogo-eventos'),

]