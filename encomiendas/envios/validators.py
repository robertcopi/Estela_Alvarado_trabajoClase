from django.core.exceptions import ValidationError
import re

def validar_peso_positivo(value):
    if value <= 0:
        raise ValidationError('El peso debe ser mayor a 0.')

def validar_codigo_encomienda(value):
    if not re.match(r'^\d+$', value):
        raise ValidationError('El código debe contener solo números.')

def validar_nro_doc_dni(value):
    if not re.match(r'^\d{8}$', value):
        raise ValidationError('El DNI debe contener exactamente 8 dígitos numéricos.')
