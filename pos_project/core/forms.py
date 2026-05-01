from django import forms
from .models import Articulo, ListaPrecio, GrupoArticulo, LineaArticulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codigo_articulo', 'codigo_barras', 'descripcion', 'presentacion', 'stock', 'grupo', 'linea']

class ListaPrecioForm(forms.ModelForm):
    class Meta:
        model = ListaPrecio
        fields = ['precio_1', 'precio_2', 'precio_3', 'precio_4', 'precio_compra', 'precio_costo']
