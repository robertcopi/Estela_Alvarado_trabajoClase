from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    mobile = models.CharField(max_length=20, blank=True, null=True)
    perfil_nombre = models.CharField(max_length=50, default="Administrador")

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Add full_name and mobile properties to User model on the fly so templates don't break
def get_full_name(self):
    return f"{self.first_name} {self.last_name}".strip() or self.username
User.add_to_class("full_name", property(get_full_name))

def get_mobile(self):
    return self.perfil.mobile if hasattr(self, 'perfil') else "No especificado"
User.add_to_class("mobile", property(get_mobile))
