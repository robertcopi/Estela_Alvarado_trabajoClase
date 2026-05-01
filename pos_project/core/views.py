from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Articulo, GrupoArticulo, LineaArticulo, ListaPrecio
from .forms import ArticuloForm, ListaPrecioForm

@login_required
def home(request):
    total_articulos = Articulo.objects.count()
    total_usuarios = User.objects.count()
    bajo_stock = Articulo.objects.filter(stock__lt=10).count()
    
    context = {
        'total_articulos': total_articulos,
        'total_usuarios': total_usuarios,
        'bajo_stock': bajo_stock,
        'ventas_hoy': 0,
    }
    return render(request, 'core/index.html', context)

@login_required
def articulos_list(request):
    articulos_list = Articulo.objects.all()
    
    q = request.GET.get('q')
    if q:
        articulos_list = articulos_list.filter(descripcion__icontains=q)
    
    paginator = Paginator(articulos_list, 15)
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)
    
    context = {
        'articulos': articulos,
    }
    return render(request, 'core/articulos/list.html', context)

@login_required
def articulo_detail(request, articulo_id):
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    
    context = {
        'articulo': articulo,
    }
    return render(request, 'core/articulos/detail.html', context)

@login_required
def articulo_create(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        precio_form = ListaPrecioForm(request.POST)
        
        if form.is_valid() and precio_form.is_valid():
            articulo = form.save()
            lista_precio = precio_form.save(commit=False)
            lista_precio.articulo = articulo
            lista_precio.save()
            
            messages.success(request, 'Artículo creado correctamente.')
            return redirect('articulo_detail', articulo_id=articulo.articulo_id)
    else:
        form = ArticuloForm()
        precio_form = ListaPrecioForm()
    
    context = {
        'form': form,
        'precio_form': precio_form,
    }
    return render(request, 'core/articulos/form.html', context)

@login_required
def articulo_edit(request, articulo_id):
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    lista_precio = get_object_or_404(ListaPrecio, articulo=articulo)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        precio_form = ListaPrecioForm(request.POST, instance=lista_precio)
        
        if form.is_valid() and precio_form.is_valid():
            form.save()
            precio_form.save()
            messages.success(request, 'Artículo actualizado correctamente.')
            return redirect('articulo_detail', articulo_id=articulo.articulo_id)
    else:
        form = ArticuloForm(instance=articulo)
        precio_form = ListaPrecioForm(instance=lista_precio)
        
    context = {
        'form': form,
        'precio_form': precio_form,
    }
    return render(request, 'core/articulos/form.html', context)
