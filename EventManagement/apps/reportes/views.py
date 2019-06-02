from django.shortcuts import render
from apps.eventos.models import Evento, EventoCategoria
from apps.compras.models import Factura
from apps.boletas.models import Boleta
from django.db.models import Avg, Max, Min, Sum
from django.db.models import F
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from apps.usuarios.models import Perfil
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class MixinGerente(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.perfil.rol == Perfil.GERENTE

class BoletasPorEventoVista(MixinGerente, BaseLineChartView):
    def get_labels(self):
        nombres_eventos = list(Evento.objects.all().values_list("nombre_evento", flat=True))
        return nombres_eventos

    def get_providers(self):
        return ["Boletas Vendidas"]

    def get_data(self):
        eventos = Evento.objects.all()
        boletas_vendidas_eventos = []
        for evento in eventos:
            boletas_vendidas_evento = evento.categorias.aggregate(Sum('boletas_vendidas'))["boletas_vendidas__sum"]
            boletas_vendidas_eventos.append(boletas_vendidas_evento)
        return [boletas_vendidas_eventos]
                
vista_boletas_por_evento = TemplateView.as_view(template_name='boletas_por_evento.html')
boletas_por_evento_json = BoletasPorEventoVista.as_view()

class DineroPorEventoVista(MixinGerente, BaseLineChartView):
    def get_labels(self):
        nombres_eventos = list(Evento.objects.all().values_list("nombre_evento", flat=True))
        return nombres_eventos

    def get_providers(self):
        return ["Dinero Total en Pesos"]

    def get_data(self):
        eventos = Evento.objects.all()
        dinero_eventos = []
        for evento in eventos:
            dinero_por_evento = evento.categorias.aggregate(total=Sum(F('boletas_vendidas') * F('precio')))['total']
            dinero_eventos.append(dinero_por_evento)
        return [dinero_eventos]

vista_dinero_por_evento = TemplateView.as_view(template_name='dinero_por_evento.html')
dinero_por_evento_json = DineroPorEventoVista.as_view()
    
def ver_facturas_evento(request, evento_id):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        evento_aux = Evento.objects.get(id = evento_id)
        categorias = EventoCategoria.objects.filter(evento = evento_aux)
        cantidad_boletas_vendidas_por_categoria = []
        for categoria in categorias:
            cantidad_boletas_vendidas_por_categoria.append(categoria.boletas_vendidas)
        boletas = Boleta.objects.filter(categoria__evento__id=evento_id)
        cantidad_boletas_vendidas_totales = boletas.count
        facturas_id = boletas.values_list("factura_ref").distinct()
        facturas = Factura.objects.filter(id__in = facturas_id)
        return render(request, 'ver_facturas_evento.html', {"facturas" : facturas, 'evento': evento_aux, 'cantidad_boletas_vendidas_por_categoria' : cantidad_boletas_vendidas_por_categoria, 'cantidad_boletas_vendidas_totales' : cantidad_boletas_vendidas_totales})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

def ver_facturas_eventos(request):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        eventos = Evento.objects.all()
        return render(request, 'ver_facturas_eventos.html', {'eventos' : eventos})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')