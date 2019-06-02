from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from apps.eventos.models import *
from apps.compras.models import *
import json
from apps.usuarios.models import Perfil

def gestionar_eventos(request):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        form = None
        if request.method == 'POST':
            form = EventoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Evento creado exitosamente')
                form = EventoForm()
            else:
                messages.error(request, 'Hay errores en el formulario, por favor corrigelos. :(')
        else:
            form = EventoForm()
        eventos = Evento.objects.all()
        return render(request, 'gestionar_eventos.html', {'form': form, 'eventos' : eventos})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

def gestionar_evento(request, evento_id):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        instancia_evento = Evento.objects.get(id = evento_id)
        if request.method == 'POST' and 'btnEvento' in request.POST:
            form_evento = EventoForm(request.POST or None, request.FILES or None, instance = instancia_evento)
            if form_evento.is_valid():
                form_evento.save()
                messages.success(request, 'Evento actualizado exitosamente')
            else:
                print(form_evento.errors)
                messages.error(request, 'Hay errores en el formulario de evento, por favor corrigelos.')
        form_evento = EventoForm(instance = instancia_evento)
        form_evento.fields['tipo_evento'].widget = forms.HiddenInput()
        return render(request, 'gestionar_evento.html', {'form_evento': form_evento})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')


def gestionar_categorias_tipo_evento(request, tipo_evento_id):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        instancia_tipo_evento = TipoEvento.objects.get(id = tipo_evento_id)
        form_categoria = CategoriaTipoEventoForm()
        editar_categoria  = False
        if request.method == 'POST' and 'btnCrear' in request.POST:
            form_categoria = CategoriaTipoEventoForm(request.POST)
            if form_categoria.is_valid():
                instancia_tipo_evento = TipoEvento.objects.get(id = tipo_evento_id)
                form_categoria.instance.tipo_evento = instancia_tipo_evento
                form_categoria.save()
                messages.success(request, 'Categoria del tipo creada exitosamente')
                form_categoria = CategoriaTipoEventoForm()
            else:
                messages.error(request, 'Hay errores en el formulario de categoria, por favor corrigelos.')
        elif request.method == 'POST' and 'btnEditar' in request.POST:
            id_aux = request.POST.get('btnEditar')
            instancia_categoria = CategoriaTipoEvento.objects.get(id=id_aux)
            form_categoria = CategoriaTipoEventoForm(instance = instancia_categoria)
            form_categoria.fields["id_aux"].initial = instancia_categoria.id
            editar_categoria = True
        elif request.method == 'POST' and 'btnActualizar' in request.POST:
            form_categoria = CategoriaTipoEventoForm(request.POST)
            if form_categoria.is_valid():
                id_aux = int(request.POST.get("id_aux"))
                instancia_categoria = CategoriaTipoEvento.objects.get(id = id_aux)
                form_categoria = CategoriaTipoEventoForm(request.POST, instance = instancia_categoria)
                form_categoria.save()
                messages.success(request, 'Tipo Evento actualizado exitosamente')
            else:
                messages.error(request, 'Hay errores en el formulario de categoria, por favor corrigelos.')
       
        instancia_tipo_evento = TipoEvento.objects.get(id = tipo_evento_id)
        categorias = instancia_tipo_evento.categorias_tipo.all()
        return render(request, 'gestionar_categorias_tipo_evento.html', {'form_categoria': form_categoria, 'categorias' : categorias, 'tipo_evento_id': tipo_evento_id, 'editar_categoria': editar_categoria})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

def gestionar_tipo_evento(request, tipo_evento_id):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        instancia_tipo_evento = TipoEvento.objects.get(id = tipo_evento_id)
        form_tipo_evento = TipoEventoForm(instance = instancia_tipo_evento)
        if request.method == 'POST' and 'btnEvento' in request.POST:
            form_tipo_evento = EventoForm(request.POST or None)
            if form_tipo_evento.is_valid():
                instancia_tipo_evento = TipoEvento.objects.get(id = tipo_evento_id)
                form_tipo_evento = TipoEventoForm(request.POST or None, instance = instancia_tipo_evento)
                form_tipo_evento.save()
                messages.success(request, 'Tipo Evento actualizado exitosamente')
            else:
                messages.error(request, 'Hay errores en el formulario de tipo evento, por favor corrigelos.')
        return render(request, 'gestionar_tipo_evento.html', {'form_tipo_evento': form_tipo_evento})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

def gestionar_categorias_evento(request, evento_id):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        instancia_evento = Evento.objects.get(id = evento_id)
        form_categoria = CategoriaEventoForm()
        editar_categoria  = False
        instancia_categoria = None
        if request.method == 'POST' and 'btnEditar' in request.POST:
            id_aux = request.POST.get('btnEditar')
            instancia_categoria = EventoCategoria.objects.get(id=id_aux)
            form_categoria = CategoriaEventoForm(instance = instancia_categoria)
            form_categoria.fields["id_aux"].initial = instancia_categoria.id
            editar_categoria = True
        elif request.method == 'POST' and 'btnActualizar' in request.POST:
            form_categoria = CategoriaEventoForm(request.POST)
            if form_categoria.is_valid():
                id_aux = int(request.POST.get("id_aux"))
                instancia_categoria = EventoCategoria.objects.get(id = id_aux)
                form_categoria = CategoriaEventoForm(request.POST, instance = instancia_categoria)
                form_categoria.save()
                messages.success(request, 'Categoria del Evento actualizado exitosamente')
            else:
                messages.error(request, 'Hay errores en el formulario de categoria, por favor corrigelos.')
        instancia_evento = Evento.objects.get(id = evento_id)
        categorias = instancia_evento.categorias.all()
        return render(request, 'gestionar_categorias_evento.html', {'form_categoria': form_categoria, 'categorias' : categorias, 'evento_id': evento_id, 'editar_categoria': editar_categoria, 'instancia_categoria' : instancia_categoria})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

def catalogo_eventos(request):
    from apps.interoperabilidad import views as w_inter
    eventos_proveedores = w_inter.obtener_eventos_proveedores()
    eventos = Evento.objects.all()
    if not(request.user.is_anonymous):
        cantidad_carrito = len(ElementoCarrito.objects.filter(usuario = request.user))
    else:
        cantidad_carrito = 0
    return render(request, 'catalogo_eventos.html', {'eventos' : eventos, "cantidad_carrito" : cantidad_carrito, 'eventos_proveedores':eventos_proveedores})

def gestionar_tipo_eventos(request):
    user = request.user
    if user.perfil.rol == Perfil.GERENTE:
        form = None
        if request.method == 'POST':
            form = TipoEventoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tipo Evento creado exitosamente')
                form = TipoEventoForm()
            else:
                messages.error(request, 'Hay errores en el formulario, por favor corrigelos. :(')
        else:
            form = TipoEventoForm()
        tipo_eventos = TipoEvento.objects.all()
        return render(request, 'gestionar_tipo_eventos.html', {'form': form, "tipo_eventos": tipo_eventos})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')