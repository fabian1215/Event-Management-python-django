from django.urls import path
from apps.boletas.views import *

app_name = 'boletas'

urlpatterns = [
    path('ver-boleta/<int:boleta_id>', ver_boleta, name='ver-boleta'),
]