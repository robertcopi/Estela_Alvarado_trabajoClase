from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ruta

class RutaListView(LoginRequiredMixin, ListView):
    model = Ruta
    template_name = 'rutas/ruta_list.html'
    context_object_name = 'rutas'

class RutaCreateView(LoginRequiredMixin, CreateView):
    model = Ruta
    template_name = 'rutas/ruta_form.html'
    fields = ['codigo', 'origen', 'destino', 'descripcion', 'precio_base', 'dias_entrega']
    success_url = reverse_lazy('ruta_list')
