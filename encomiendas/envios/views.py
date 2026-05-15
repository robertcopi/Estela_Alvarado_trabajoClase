from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Encomienda, HistorialEstado
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

@login_required
def dashboard_rt(request):
    # This renders the real-time dashboard template
    return render(request, 'envios/dashboard_rt.html')

@login_required
def cambiar_estado(request, pk):
    if request.method == 'POST':
        encomienda = get_object_or_404(Encomienda, pk=pk)
        nuevo_estado = request.POST.get('nuevo_estado')
        
        if nuevo_estado in dict(EstadoEnvio.choices):
            encomienda.estado = nuevo_estado
            encomienda.save()
            
            from .models import Empleado, HistorialEstado
            empleado = Empleado.objects.first()
            if not empleado:
                empleado = Empleado.objects.create(nombres='Admin', apellidos='Sistema', nro_doc='00000000')
                
            HistorialEstado.objects.create(
                encomienda=encomienda,
                estado_nuevo=nuevo_estado,
                empleado=empleado,
                observacion="Estado actualizado mediante acciones rápidas."
            )
            messages.success(request, f"Estado actualizado a {encomienda.get_estado_display()}")
            
    return redirect('encomienda_detail', pk=pk)

class EncomiendaCreateView(LoginRequiredMixin, CreateView):
    model = Encomienda
    template_name = 'envios/encomiendas/form.html'
    fields = ['codigo', 'descripcion', 'peso_kg', 'remitente', 'destinatario', 'ruta']
    success_url = reverse_lazy('encomiendas_list')

    def form_valid(self, form):
        encomienda = form.save(commit=False)
        encomienda.estado = EstadoEnvio.PENDIENTE
        
        # Asignar empleado_registra
        from .models import Empleado
        empleado = Empleado.objects.first() # Temporalmente asignado
        if not empleado:
            empleado = Empleado.objects.create(nombres='Admin', apellidos='Sistema', nro_doc='00000000')
        encomienda.empleado_registra = empleado
        encomienda.save()
        
        # Registrar el historial inicial
        HistorialEstado.objects.create(
            encomienda=encomienda,
            estado_nuevo=EstadoEnvio.PENDIENTE,
            empleado=empleado,
            observacion="Ingresado desde el sistema web."
        )
        return super().form_valid(form)
