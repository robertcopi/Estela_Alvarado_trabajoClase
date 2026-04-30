from django.db import models
from config.choices import EstadoGeneral

class Ruta(models.Model):
    codigo = models.CharField('Código de Ruta', max_length=10, unique=True)
    origen = models.CharField('Origen', max_length=100)
    destino = models.CharField('Destino', max_length=100)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    precio_base = models.DecimalField('Precio Base', max_digits=8, decimal_places=2)
    dias_entrega = models.PositiveIntegerField('Días de Entrega Estimados')
    estado = models.CharField('Estado', max_length=2, choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO)

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['origen', 'destino']

    def __str__(self):
        return f"{self.codigo} - {self.origen} a {self.destino}"
