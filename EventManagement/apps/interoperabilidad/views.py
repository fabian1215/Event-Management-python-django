from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import *
from apps.eventos.models import Evento
from django.urls import reverse
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.usuarios.models import Perfil
import requests

class MixinAdministrador(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.perfil.rol == Perfil.ADMINISTRADOR

class ProveedorEventosListar(MixinAdministrador, ListView): 
    model =  ProveedorEventos

class ProveedorEventosDetalle(MixinAdministrador, DetailView): 
    model = ProveedorEventos

class ProveedorEventosCrear(MixinAdministrador, SuccessMessageMixin, CreateView): 
    model = ProveedorEventos
    fields = '__all__'
    success_message = 'Proveedor de eventos agregado con exito'
    def get_success_url(self, **kwargs):         
        return reverse_lazy("interoperabilidad:proveedor_eventos_listar")

class ProveedorEventosActualizar(MixinAdministrador, SuccessMessageMixin, UpdateView): 
    model = ProveedorEventos
    success_message = 'Proveedor de eventos  modificado con exito'
    fields = '__all__'
    def get_success_url(self, **kwargs):         
        return reverse_lazy("interoperabilidad:proveedor_eventos_listar")

class ProveedorEventosEliminar(MixinAdministrador, DeleteView): 
    model = ProveedorEventos

def obtener_eventos_proveedores():
    proveedores = ProveedorEventos.objects.all()
    eventos_proveedores = []
    for proveedor in proveedores:
        api_url = proveedor.api_url
        try:
            resp = requests.get(url=api_url, params={})
        except requests.exceptions.RequestException as e:
            print("para la url " + api_url + ": ")
            print(e)
            resp = None
        if resp != None:
            data = resp.json()
            eventos_proveedores.append({"proveedor_nombre":proveedor.nombre, "proveedor_id":proveedor.id, "data" : data})
    return eventos_proveedores

def eventos_json(request):
    json = []
    eventos = Evento.objects.all()
    URL_SERVIDOR = "http://localhost:8000"
    for evento in eventos:
        evento_json = {}
        evento_json["nombre"] = evento.nombre_evento
        evento_json["fecha"] = evento.fecha_hora.strftime('%Y-%m-%d')
        evento_json["hora"] = evento.fecha_hora.strftime('%H:%M')
        evento_json["lugar"] = evento.lugar_realizacion
        evento_json["url"] = URL_SERVIDOR + reverse("compras:agregar-boletas-evento-carrito", kwargs={'id_evento':evento.id})
        
        categorias = evento.categorias.all()
        minimo = categorias.aggregate(Min('precio'))["precio__min"]
        maximo = categorias.aggregate(Max('precio'))["precio__max"]
        if minimo == None:
            minimo = 0
        if maximo == None:
            maximo = 0
        evento_json["valor_minimo"] = str(minimo)
        evento_json["valor_maximo"] = str(maximo)
        json.append(evento_json)
    return JsonResponse(json, safe=False, json_dumps_params={'ensure_ascii':False})