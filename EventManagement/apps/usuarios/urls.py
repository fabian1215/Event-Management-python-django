from django.urls import path
from apps.usuarios.views import *

app_name = 'usuarios'

urlpatterns = [
    path('home/', home, name='home'),
    path('listar-usuarios', UsuariosListar.as_view(), name='listar_usuarios'),
]