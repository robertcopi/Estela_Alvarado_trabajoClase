from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Encomienda
from clientes.models import Cliente
from config.choices import EstadoEnvio

@login_required
def home(request):
    hoy = timezone.now().date()
    
    total_encomiendas = Encomienda.objects.count()
    envios_hoy = Encomienda.objects.filter(fecha_envio__date=hoy).count()
    total_clientes = Cliente.objects.count()
    entregas_pendientes = Encomienda.objects.exclude(estado=EstadoEnvio.ENTREGADO).count()
    
    context = {
        'total_encomiendas': total_encomiendas,
        'envios_hoy': envios_hoy,
        'total_clientes': total_clientes,
        'entregas_pendientes': entregas_pendientes,
    }
    return render(request, 'envios/index.html', context)

@login_required
def encomiendas_list(request):
    encomiendas_list = Encomienda.objects.all()
    
    q = request.GET.get('q')
    if q:
        encomiendas_list = encomiendas_list.filter(codigo__icontains=q)
        
    paginator = Paginator(encomiendas_list, 15)
    page_number = request.GET.get('page')
    encomiendas = paginator.get_page(page_number)
    
    context = {
        'encomiendas': encomiendas,
    }
    return render(request, 'envios/encomiendas/list.html', context)

@login_required
def encomienda_detail(request, pk):
    encomienda = get_object_or_404(Encomienda, pk=pk)
    context = {
        'encomienda': encomienda,
    }
    return render(request, 'envios/encomiendas/detail.html', context)
