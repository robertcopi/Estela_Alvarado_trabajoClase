from django.db import models
from config.choices import EstadoGeneral, TipoDocumento

class Cliente(models.Model):
    tipo_doc = models.CharField('Tipo de Documento', max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.DNI)
    nro_doc = models.CharField('Número de Documento', max_length=15, unique=True)
    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    telefono = models.CharField('Teléfono', max_length=15, blank=True, null=True)
    email = models.EmailField('Correo Electrónico', blank=True, null=True)
    direccion = models.TextField('Dirección', blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO)
    fecha_registro = models.DateTimeField('Fecha de Registro', auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.nro_doc}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def esta_activo(self):
        return self.estado == EstadoGeneral.ACTIVO

    @property
    def total_encomiendas_enviadas(self):
        return self.encomiendas_enviadas.count()
