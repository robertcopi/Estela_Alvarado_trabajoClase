from django.db import models

class EstadoGeneral(models.TextChoices):
    ACTIVO = 'AC', 'Activo'
    INACTIVO = 'IN', 'Inactivo'

class EstadoEnvio(models.TextChoices):
    PENDIENTE = 'PE', 'Pendiente'
    EN_TRANSITO = 'TR', 'En tránsito'
    ENTREGADO = 'EN', 'Entregado'
    DEVUELTO = 'DE', 'Devuelto'

class TipoDocumento(models.TextChoices):
    DNI = 'DNI', 'DNI'
    RUC = 'RUC', 'RUC'
    CE = 'CE', 'Carné de Extranjería'
    PASAPORTE = 'PAS', 'Pasaporte'
