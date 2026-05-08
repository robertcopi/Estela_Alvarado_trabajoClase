from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid
from datetime import datetime

from .models import Articulo, GrupoArticulo, LineaArticulo, ListaPrecio, OrdenCompraCliente, ItemOrdenCompraCliente
from pos_project.choices import EstadoOrden
from .forms import ArticuloForm, ListaPrecioForm
from .cart import Cart

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
    
    # Recently viewed session logic
    recently_viewed = request.session.get('recently_viewed', [])
    str_id = str(articulo_id)
    if str_id in recently_viewed:
        recently_viewed.remove(str_id)
    recently_viewed.insert(0, str_id)
    request.session['recently_viewed'] = recently_viewed[:5]  # Keep last 5
    
    recently_viewed_articulos = Articulo.objects.filter(articulo_id__in=recently_viewed)
    
    context = {
        'articulo': articulo,
        'recently_viewed_articulos': recently_viewed_articulos,
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

# --- Cart Views ---

@login_required
def cart_add(request, articulo_id):
    cart = Cart(request)
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        update = request.POST.get('update', False) == 'True'
        cart.add(articulo=articulo, cantidad=cantidad, update_quantity=update)
        messages.success(request, f'{articulo.descripcion} ha sido añadido al carrito.')
    return redirect('cart_detail')

@login_required
def cart_remove(request, articulo_id):
    cart = Cart(request)
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    cart.remove(articulo)
    messages.info(request, f'{articulo.descripcion} ha sido eliminado del carrito.')
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'El carrito ha sido vaciado.')
    return redirect('cart_detail')

# --- Checkout and Order Views ---

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('cart_detail')
        
    if request.method == 'POST':
        # Create order
        nro_pedido = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        orden = OrdenCompraCliente.objects.create(
            nro_pedido=nro_pedido,
            cliente=request.user,
            importe=cart.get_total_price(),
            estado=EstadoOrden.PENDIENTE,
            creado_por=request.user
        )
        
        nro_item = 1
        for item in cart:
            ItemOrdenCompraCliente.objects.create(
                orden=orden,
                articulo=item['articulo'],
                nro_item=nro_item,
                cantidad=item['cantidad'],
                precio_unitario=item['precio'],
                total_item=item['total_precio']
            )
            nro_item += 1
            
        cart.clear()
        send_order_confirmation_email(request, orden)
        messages.success(request, 'Orden creada exitosamente.')
        return redirect('order_detail', pedido_id=orden.pedido_id)

    return render(request, 'cart/checkout.html', {'cart': cart})

@login_required
def order_detail(request, pedido_id):
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id, cliente=request.user)
    return render(request, 'cart/order_detail.html', {'orden': orden})

def send_order_confirmation_email(request, orden):
    subject = f'Confirmación de Orden #{orden.nro_pedido}'
    message = render_to_string('emails/order_confirmation.html', {'orden': orden})
    try:
        send_mail(
            subject,
            '',
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=True,
            html_message=message
        )
    except Exception as e:
        print(f"Error sending email: {e}")

@login_required
def generate_pdf_order(request, pedido_id):
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id, cliente=request.user)
    # Placeholder for PDF generation
    # Normally you'd use reportlab or weasyprint
    return HttpResponse(f"PDF generado para la orden {orden.nro_pedido}")

@login_required
def cancel_order(request, pedido_id):
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id, cliente=request.user)
    if orden.estado == EstadoOrden.PENDIENTE:
        orden.estado = EstadoOrden.CANCELADO
        orden.save()
        messages.success(request, 'Orden cancelada exitosamente.')
    else:
        messages.error(request, 'No se puede cancelar esta orden.')
    return redirect('order_detail', pedido_id=orden.pedido_id)

# --- API ---

def api_articulos(request):
    articulos_list = Articulo.objects.all()
    q = request.GET.get('q')
    if q:
        articulos_list = articulos_list.filter(descripcion__icontains=q)
    
    paginator = Paginator(articulos_list, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    data = []
    for art in page_obj:
        try:
            precio = art.listaprecio.precio_1
        except:
            precio = 0
            
        data.append({
            'articulo_id': str(art.articulo_id),
            'descripcion': art.descripcion,
            'codigo_articulo': art.codigo_articulo,
            'precio': str(precio),
        })
        
    return JsonResponse({
        'results': data,
        'has_next': page_obj.has_next(),
    })

