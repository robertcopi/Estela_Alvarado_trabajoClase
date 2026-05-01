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

print("Initial data created successfully.")
