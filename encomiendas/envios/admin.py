from django.contrib import admin
from .models import Empleado, Encomienda, HistorialEstado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nro_doc', 'nombres', 'apellidos', 'estado')
    list_filter = ('estado',)

class HistorialEstadoInline(admin.TabularInline):
    model = HistorialEstado
    extra = 1

@admin.register(Encomienda)
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'remitente', 'destinatario', 'peso_kg', 'estado', 'fecha_envio', 'precio_total')
    list_filter = ('estado', 'ruta')
    search_fields = ('codigo', 'remitente__nro_doc', 'destinatario__nro_doc')
    inlines = [HistorialEstadoInline]

@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ('encomienda', 'estado_anterior', 'estado_nuevo', 'fecha_cambio', 'empleado')
    list_filter = ('estado_nuevo',)
    search_fields = ('encomienda__codigo',)
