from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from config.choices import EstadoEnvio, EstadoGeneral, TipoDocumento
from clientes.models import Cliente
from rutas.models import Ruta
from .validators import validar_peso_positivo, validar_codigo_encomienda
from .querysets import EncomiendaQuerySet

class Empleado(models.Model):
    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    nro_doc = models.CharField('Número de Documento', max_length=15, unique=True)
    estado = models.CharField('Estado', max_length=2, choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Encomienda(models.Model):
    codigo = models.CharField('Código', max_length=20, unique=True, validators=[validar_codigo_encomienda])
    descripcion = models.TextField('Descripción')
    peso_kg = models.DecimalField('Peso (Kg)', max_digits=8, decimal_places=2, validators=[validar_peso_positivo])
    estado = models.CharField('Estado', max_length=2, choices=EstadoEnvio.choices, default=EstadoEnvio.PENDIENTE)
    
    remitente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='encomiendas_enviadas')
    destinatario = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='encomiendas_recibidas')
    ruta = models.ForeignKey(Ruta, on_delete=models.RESTRICT, related_name='encomiendas')
    empleado_registra = models.ForeignKey(Empleado, on_delete=models.RESTRICT, related_name='encomiendas_registradas')
    
    fecha_envio = models.DateTimeField('Fecha de Envío', auto_now_add=True)
    fecha_entrega = models.DateTimeField('Fecha de Entrega', null=True, blank=True)
    precio_total = models.DecimalField('Precio Total', max_digits=8, decimal_places=2, null=True, blank=True)

    objects = EncomiendaQuerySet.as_manager()

    class Meta:
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.codigo} — {self.get_estado_display()}"

    def clean(self):
        try:
            if getattr(self, 'remitente_id', None) and getattr(self, 'destinatario_id', None):
                if self.remitente_id == self.destinatario_id:
                    raise ValidationError("El remitente no puede ser el mismo destinatario.")
        except Exception:
            pass
        
        if self.peso_kg and self.peso_kg > 50:
             raise ValidationError({"peso_kg": "El peso máximo permitido es de 50 Kg."})
        super().clean()

    def save(self, *args, **kwargs):
        if not self.precio_total and self.ruta and self.peso_kg:
            self.precio_total = self.calcular_costo()
        super().save(*args, **kwargs)

    def calcular_costo(self):
        from decimal import Decimal
        return self.ruta.precio_base + (Decimal(str(self.peso_kg)) * Decimal('2'))

    @property
    def esta_entregada(self):
        return self.estado == EstadoEnvio.ENTREGADO

    @property
    def esta_en_transito(self):
        return self.estado == EstadoEnvio.EN_TRANSITO
        
    @property
    def tiene_retraso(self):
        if not self.esta_entregada and self.ruta:
            dias_transcurridos = (timezone.now() - self.fecha_envio).days
            return dias_transcurridos > self.ruta.dias_entrega
        return False

    def cambiar_estado(self, nuevo_estado, empleado, observacion=""):
        self.estado = nuevo_estado
        if nuevo_estado == EstadoEnvio.ENTREGADO:
            self.fecha_entrega = timezone.now()
        self.save()
        HistorialEstado.objects.create(
            encomienda=self,
            estado_anterior=self.estado,
            estado_nuevo=nuevo_estado,
            empleado=empleado,
            observacion=observacion
        )

    @classmethod
    def crear_con_costo_calculado(cls, **kwargs):
        encomienda = cls(**kwargs)
        encomienda.full_clean()
        encomienda.save()
        return encomienda

class HistorialEstado(models.Model):
    encomienda = models.ForeignKey(Encomienda, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=2, choices=EstadoEnvio.choices, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Historial de Estado'
        verbose_name_plural = 'Historiales de Estados'
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f"{self.encomienda.codigo} a {self.get_estado_nuevo_display()}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=HistorialEstado)
def broadcast_estado_encomienda(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'dashboard',
            {
                'type': 'dashboard_actualizar',
                'mensaje': f'La encomienda {instance.encomienda.codigo} ha cambiado al estado: {instance.get_estado_nuevo_display()}',
                'datos': {
                    'codigo': instance.encomienda.codigo,
                    'estado': instance.get_estado_nuevo_display(),
                    'observacion': instance.observacion or '',
                    'fecha': instance.fecha_cambio.strftime("%d/%m/%Y %H:%M:%S")
                }
            }
        )
