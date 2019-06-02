from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    CLIENTE = "CLI"
    VENDEDOR = "VEN"
    GERENTE = "GER"
    ADMINISTRADOR = "ADM"
    OPCIONES_ROLES = (
        (VENDEDOR, "Vendedor"),
        (ADMINISTRADOR, "Administrador"),
        (CLIENTE, "Cliente"),
        (GERENTE, "Gerente"),
    )
    rol = models.CharField(max_length = 200, choices=OPCIONES_ROLES, default=CLIENTE)
    usuario =  models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")

    @receiver(post_save, sender=User)
    def crear_perfil(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(usuario=instance)

    def es_cliente():
        return rol == CLIENTE
    
    def es_vendedor():
        return rol == VENDEDOR
    
    def es_gerente():
        return rol == GERENTE

    def es_administrador():
        return rol == ADMINISTRADOR
        
