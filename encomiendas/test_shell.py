from clientes.models import Cliente
from rutas.models import Ruta
from envios.models import Empleado, Encomienda, HistorialEstado
from django.core.exceptions import ValidationError

print("--- INICIANDO PRUEBAS DE MODELOS ---")

# 1. Crear instancias de prueba
cliente1, _ = Cliente.objects.get_or_create(nro_doc='12345678', defaults={'nombres':'Juan', 'apellidos':'Perez', 'email':'juan@test.com'})
cliente2, _ = Cliente.objects.get_or_create(nro_doc='87654321', defaults={'nombres':'Maria', 'apellidos':'Gomez', 'email':'maria@test.com'})
ruta1, _ = Ruta.objects.get_or_create(codigo='R-01', defaults={'origen':'Lima', 'destino':'Trujillo', 'precio_base':15.00, 'dias_entrega':2})
empleado1, _ = Empleado.objects.get_or_create(nro_doc='44556677', defaults={'nombres':'Carlos', 'apellidos':'Ruiz'})

print("Instancias base creadas correctamente.")

# 2. Prueba Exitosa (classmethod)
try:
    encomienda_ok = Encomienda.crear_con_costo_calculado(
        codigo='ENC-000001',
        descripcion='Caja de zapatos',
        peso_kg=5.00,
        remitente=cliente1,
        destinatario=cliente2,
        ruta=ruta1,
        empleado_registra=empleado1
    )
    print(f"ÉXITO: Se creó la encomienda {encomienda_ok.codigo} con costo {encomienda_ok.precio_total}")
except Exception as e:
    print(f"ERROR inesperado al crear: {e}")

# 3. Fallas Forzadas
print("\n--- PROBANDO VALIDACIONES (FALLAS FORZADAS) ---")

# Falla 1: Peso negativo
try:
    Encomienda.crear_con_costo_calculado(
        codigo='ENC-000002', descripcion='Caja', peso_kg=-2.00,
        remitente=cliente1, destinatario=cliente2, ruta=ruta1, empleado_registra=empleado1
    )
except ValidationError as e:
    print(f"Falla atrapada correctamente (Peso negativo): {e}")

# Falla 2: Mismo remitente y destinatario
try:
    Encomienda.crear_con_costo_calculado(
        codigo='ENC-000003', descripcion='Doc', peso_kg=1.00,
        remitente=cliente1, destinatario=cliente1, ruta=ruta1, empleado_registra=empleado1
    )
except ValidationError as e:
    print(f"Falla atrapada correctamente (Mismo remitente/dest): {e}")

# Falla 3: Formato código incorrecto
try:
    Encomienda.crear_con_costo_calculado(
        codigo='123', descripcion='Doc', peso_kg=1.00,
        remitente=cliente1, destinatario=cliente2, ruta=ruta1, empleado_registra=empleado1
    )
except ValidationError as e:
    print(f"Falla atrapada correctamente (Formato de código): {e}")

# 4. Cambio de estado y creación en Historial
print("\n--- PROBANDO HISTORIAL DE ESTADOS ---")
encomienda_ok.cambiar_estado('TR', empleado1, "Saliendo de la agencia")
historial = HistorialEstado.objects.filter(encomienda=encomienda_ok).first()

if historial and historial.estado_nuevo == 'TR':
    print(f"ÉXITO: Historial registrado. Nuevo estado: {historial.get_estado_nuevo_display()} - Obs: {historial.observacion}")
else:
    print("ERROR: El historial no se guardó correctamente.")

print("\n--- PRUEBAS FINALIZADAS ---")
