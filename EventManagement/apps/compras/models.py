from django.db import models
from apps.eventos.models import Evento
from apps.eventos.models import EventoCategoria
from django.contrib.auth.models import User

class ElementoCarrito(models.Model):
    cedula = models.CharField(max_length = 200)
    categoria =  models.ForeignKey(EventoCategoria, on_delete=models.CASCADE)
    usuario =  models.ForeignKey(User, on_delete=models.CASCADE)

class Factura(models.Model):
    usuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(null=False)
    EFECTIVO = "EFE"
    CHEQUE = "CHE"
    TARJETA_CREDITO = "TJC"
    TARJETA_DEBITO = "TJD"
    FISICO = ('Fisico', (
        (EFECTIVO, 'Efectivo'),
        (CHEQUE, 'Cheque'),
    ))
    VIRTUAL = ('Virtual', (
        (TARJETA_CREDITO, 'Tarjeta Credito '),
        (TARJETA_DEBITO, 'Tarjeta Debito'),
    ))
    OPCIONES_PAGO = (FISICO, VIRTUAL)
    metodo_pago = models.CharField(choices=OPCIONES_PAGO, max_length=100)