from django.db import models

class EstadoOrden(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    PROCESANDO = 'PROCESANDO', 'Procesando'
    ENVIADO = 'ENVIADO', 'Enviado'
    ENTREGADO = 'ENTREGADO', 'Entregado'
    CANCELADO = 'CANCELADO', 'Cancelado'
