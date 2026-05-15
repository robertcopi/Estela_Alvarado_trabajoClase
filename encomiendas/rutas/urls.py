from django.urls import path
from . import views

urlpatterns = [
    path('', views.RutaListView.as_view(), name='ruta_list'),
    path('nueva/', views.RutaCreateView.as_view(), name='ruta_create'),
]
