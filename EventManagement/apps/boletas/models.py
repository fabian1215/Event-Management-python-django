from django.db import models
from apps.eventos.models import EventoCategoria
from apps.compras.models import Factura
from django.contrib.auth.models import User

class Boleta(models.Model):
    categoria = models.ForeignKey(EventoCategoria, on_delete = models.CASCADE, related_name = "boletas")
    factura_ref = models.ForeignKey(Factura, on_delete = models.CASCADE, related_name = "boletas_compradas")
    precio_comprado = models.PositiveIntegerField()
    cedula = models.CharField(max_length = 200)
    