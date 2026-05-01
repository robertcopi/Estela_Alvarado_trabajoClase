import uuid
from django.db import models

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
