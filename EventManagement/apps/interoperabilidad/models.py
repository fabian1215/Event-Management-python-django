from django.db import models

class ProveedorEventos(models.Model):
    nombre = models.CharField(max_length = 300)
    api_url = models.CharField(max_length = 300)