from django.db import models
from django.dispatch import receiver

class TipoEvento(models.Model):
    nombre = models.CharField(max_length = 200)
    def __str__(self):
        return self.nombre

class Evento(models.Model):
    nombre_evento = models.CharField(max_length = 200)
    fecha_hora = models.DateTimeField(null=False)
    lugar_realizacion = models.CharField(max_length = 200) # Convertir a modelo
    activo = models.BooleanField()
    imagen = models.FileField(upload_to='eventos_imagenes/', null=True, blank=True)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)

@receiver(models.signals.post_save, sender=Evento)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        categorias_tipo = instance.tipo_evento.categorias_tipo.all()
        for categoria_tipo in categorias_tipo:
            evento_categoria = EventoCategoria()
            evento_categoria.evento = instance
            evento_categoria.categoria = categoria_tipo
            evento_categoria.boletas_vendidas = 0
            evento_categoria.save()

class CategoriaTipoEvento(models.Model):
    nombre = models.CharField(max_length = 200)
    sillas_disponibles = models.PositiveIntegerField() 
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name="categorias_tipo")

class EventoCategoria(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='categorias')
    categoria = models.ForeignKey(CategoriaTipoEvento, on_delete=models.CASCADE)
    boletas_vendidas = models.PositiveIntegerField(default=0) 
    precio = models.IntegerField(default=0)