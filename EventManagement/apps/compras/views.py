from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.usuarios.models import Perfil
from apps.compras.models import *
from apps.compras.forms import MetodoPagoForm
from apps.eventos.models import *
from apps.boletas.models import *
import json
import datetime

@login_required
def agregar_boletas_evento_carrito(request, id_evento):
    user = request.user
    if user.perfil.rol == Perfil.CLIENTE or user.perfil.rol == Perfil.VENDEDOR:
        form = None
        if request.method == 'POST':
            lista_elementos = request.POST.getlist('datos')
            for elemento in lista_elementos:
                dic = json.loads(elemento)
                elemento_carrito_aux = ElementoCarrito()
                elemento_carrito_aux.usuario = request.user
                elemento_carrito_aux.cedula = dic["cedula"]
                categoria_aux = EventoCategoria.objects.get(id=int(dic["categoria_id"]))
                elemento_carrito_aux.categoria = categoria_aux
                elemento_carrito_aux.save()
            return redirect('eventos:catalogo-eventos')
        else:
            evento = Evento.objects.get(id = int(id_evento))
            categorias = evento.categorias.all()
            return render(request, 'agregar_boletas_evento_carrito.html', {'evento' : evento, 'categorias' : categorias})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

@login_required
def carrito_compras(request):
    user = request.user
    if user.perfil.rol == Perfil.CLIENTE or user.perfil.rol == Perfil.VENDEDOR:
        form = None
        if request.method == 'POST':
            elementos_carrito = ElementoCarrito.objects.filter(usuario = request.user)
            factura_aux = Factura()
            factura_aux.fecha_hora = datetime.datetime.now()
            factura_aux.usuario = request.user
            factura_aux.metodo_pago = request.POST.get("metodo_pago")
            print(request.POST.get("metodo_pago"))
            factura_aux.save()
            boletas = []
            flag_error = False
            for elemento in elementos_carrito:
                boleta_aux = Boleta()
                boleta_aux.categoria = elemento.categoria
                boleta_aux.precio_comprado = elemento.categoria.precio # por si el precio cambia
                boleta_aux.cedula = elemento.cedula
                boletas.append(boleta_aux)
                sillas_disponibles = elemento.categoria.categoria.sillas_disponibles - elemento.categoria.boletas_vendidas
                if sillas_disponibles <= 0:
                    flag_error = True
                    messages.error(request, 'El evento ' + elemento.categoria.evento.nombre_evento + ' no tiene sillas disponibles para la categoria ' + elemento.categoria.nombre)
            if(not flag_error and len(elementos_carrito)!=0):
                factura_aux.save()
                for boleta in boletas:
                    boleta.factura_ref = factura_aux
                    boleta.save()
                    categoria_aux = EventoCategoria.objects.get(id = boleta.categoria.id)
                    categoria_aux.boletas_vendidas = categoria_aux.boletas_vendidas + 1
                    categoria_aux.save()
                #vaciar carrito de compras
                for elemento in elementos_carrito:
                    elemento.delete()
            if len(elementos_carrito) == 0:
                messages.error(request, 'No hay elementos en el carrito de compras')
            #return redirect('compras:catalogo-boletas')
        metodo_pago_form = MetodoPagoForm()
        if user.perfil.rol == Perfil.VENDEDOR:
            opciones = (Factura.FISICO, Factura.VIRTUAL)
        else:
            opciones =  (Factura.VIRTUAL, Factura.VIRTUAL)

        metodo_pago_form.fields['metodo_pago'].choices = opciones
        elementos_carrito = ElementoCarrito.objects.filter(usuario = request.user)
        cantidad_carrito = len(ElementoCarrito.objects.filter(usuario = request.user))
        return render(request, 'carrito_compras.html', {'elementos_carrito' : elementos_carrito, 'cantidad_carrito' : cantidad_carrito, 'metodo_pago_form':metodo_pago_form})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

@login_required
def ver_factura(request, id_factura):
    user = request.user
    factura_pertenece_cliente = True # IMPLEMENTAR
    if factura_pertenece_cliente or user.perfil.rol == Perfil.VENDEDOR or user.perfil.rol == Perfil.GERENTE:
        factura = Factura.objects.get(id = id_factura)
        boletas_compradas = factura.boletas_compradas.all()
        precio_total = 0
        for boleta_comprada in boletas_compradas:
            precio_total = precio_total + boleta_comprada.precio_comprado
        return render(request, 'ver_factura.html', {'factura' : factura, 'boletas_compradas' : boletas_compradas, 'precio_total' : precio_total})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

@login_required
def mis_compras(request):
    user = request.user
    if user.perfil.rol == Perfil.CLIENTE or user.perfil.rol == Perfil.VENDEDOR:
        facturas = Factura.objects.filter(usuario = request.user)
        return render(request, 'mis_compras.html', {"facturas" : facturas})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')

@login_required
def eliminar_elemento_carrito(request, elemento_id):
    # user = request.user
    # Validar que el usuario
    if user.perfil.rol == Perfil.CLIENTE or user.perfil.rol == Perfil.VENDEDOR:
        elemento_aux = ElementoCarrito.objects.get(id=elemento_id)
        elemento_aux.delete()
        return redirect('compras:carrito-compras')
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('eventos:catalogo-eventos')