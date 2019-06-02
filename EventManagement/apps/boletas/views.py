from django.shortcuts import render
from apps.boletas.models import Boleta

def ver_boleta(request, boleta_id):
    user = request.user
    boleta_pertenece_cliente = True #IMPLEMENTAR
    if boleta_pertenece_cliente or user.perfil.rol == Perfil.VENDEDOR or user.perfil.rol == Perfil.GERENTE:
        boleta_aux = Boleta.objects.get(id=boleta_id)
        return render(request, 'ver-boleta.html', {'boleta' : boleta_aux})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')
