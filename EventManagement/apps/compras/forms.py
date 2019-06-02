from django import forms
from apps.eventos.models import *
from apps.compras.models import *

class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ('metodo_pago',)