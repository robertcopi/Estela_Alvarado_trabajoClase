from django.db import models
from config.choices import EstadoEnvio, EstadoGeneral

class ClienteQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(estado=EstadoGeneral.ACTIVO)

    def buscar(self, query):
        return self.filter(
            models.Q(nombres__icontains=query) |
            models.Q(apellidos__icontains=query) |
            models.Q(nro_doc__icontains=query)
        )

class RutaQuerySet(models.QuerySet):
    def activas(self):
        return self.filter(estado=EstadoGeneral.ACTIVO)

class EncomiendaQuerySet(models.QuerySet):
    def pendientes(self):
        return self.filter(estado=EstadoEnvio.PENDIENTE)

    def en_transito(self):
        return self.filter(estado=EstadoEnvio.EN_TRANSITO)

    def por_ruta(self, ruta_id):
        return self.filter(ruta_id=ruta_id)

    def entregadas(self):
        return self.filter(estado=EstadoEnvio.ENTREGADO)
