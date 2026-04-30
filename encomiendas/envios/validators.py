from django.core.exceptions import ValidationError
import re

def validar_peso_positivo(value):
    if value <= 0:
        raise ValidationError('El peso debe ser mayor a 0.')

def validar_codigo_encomienda(value):
    if not re.match(r'^ENC-\d{6}$', value):
        raise ValidationError('El código debe tener el formato ENC-XXXXXX (ej. ENC-000123).')

def validar_nro_doc_dni(value):
    if not re.match(r'^\d{8}$', value):
        raise ValidationError('El DNI debe contener exactamente 8 dígitos numéricos.')
