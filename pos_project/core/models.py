import uuid
from django.db import models
from django.contrib.auth.models import User
from pos_project.choices import EstadoOrden

class GrupoArticulo(models.Model):
    nombre_grupo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_grupo

class LineaArticulo(models.Model):
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.CASCADE)
    nombre_linea = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_linea

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_articulo = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=200)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(default=0)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.CASCADE)
    linea = models.ForeignKey(LineaArticulo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo_articulo} - {self.descripcion}"

class ListaPrecio(models.Model):
    articulo = models.OneToOneField(Articulo, on_delete=models.CASCADE, related_name='listaprecio')
    precio_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    precio_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    precio_4 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Precios - {self.articulo.descripcion}"

class OrdenCompraCliente(models.Model):
    pedido_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nro_pedido = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_cliente')
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_vendedor')
    importe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=EstadoOrden.choices, default=EstadoOrden.PENDIENTE)
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.nro_pedido} - {self.cliente.username}"

class ItemOrdenCompraCliente(models.Model):
    orden = models.ForeignKey(OrdenCompraCliente, on_delete=models.CASCADE, related_name='items')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    nro_item = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.nro_item} - {self.articulo.descripcion}"

