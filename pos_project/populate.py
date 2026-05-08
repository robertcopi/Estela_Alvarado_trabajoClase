from django.contrib.auth.models import User
from core.models import GrupoArticulo, LineaArticulo
from accounts.models import Perfil

# Create Superuser
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    user.first_name = "Administrador"
    user.last_name = "Principal"
    user.save()
    
    # Create profile
    Perfil.objects.create(user=user, mobile="987654321", perfil_nombre="Administrador General")
    print("Superuser 'admin' created with password 'admin123'.")

# Create initial groups and lines
grupo1, _ = GrupoArticulo.objects.get_or_create(nombre_grupo="Abarrotes")
grupo2, _ = GrupoArticulo.objects.get_or_create(nombre_grupo="Bebidas")

LineaArticulo.objects.get_or_create(nombre_linea="Cereales y Pastas", grupo=grupo1)
LineaArticulo.objects.get_or_create(nombre_linea="Lácteos", grupo=grupo1)
LineaArticulo.objects.get_or_create(nombre_linea="Gaseosas", grupo=grupo2)
LineaArticulo.objects.get_or_create(nombre_linea="Jugos", grupo=grupo2)

from core.models import Articulo, ListaPrecio

# Create some dummy articles
if Articulo.objects.count() == 0:
    import uuid
    linea1 = LineaArticulo.objects.get(nombre_linea="Cereales y Pastas")
    linea2 = LineaArticulo.objects.get(nombre_linea="Lácteos")
    linea3 = LineaArticulo.objects.get(nombre_linea="Gaseosas")

    art1 = Articulo.objects.create(codigo_articulo="ART001", descripcion="Fideos Spaghetti 500g", stock=50, grupo=grupo1, linea=linea1)
    ListaPrecio.objects.create(articulo=art1, precio_1=3.50, precio_compra=2.00, precio_costo=2.10)

    art2 = Articulo.objects.create(codigo_articulo="ART002", descripcion="Leche Evaporada 400g", stock=100, grupo=grupo1, linea=linea2)
    ListaPrecio.objects.create(articulo=art2, precio_1=4.20, precio_compra=3.00, precio_costo=3.10)

    art3 = Articulo.objects.create(codigo_articulo="ART003", descripcion="Gaseosa Cola 3L", stock=30, grupo=grupo2, linea=linea3)
    ListaPrecio.objects.create(articulo=art3, precio_1=9.00, precio_compra=6.50, precio_costo=6.80)

    print("Dummy articles created successfully.")

print("Initial data created successfully.")
