from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('encomiendas/', views.encomiendas_list, name='encomiendas_list'),
    path('encomiendas/<int:pk>/', views.encomienda_detail, name='encomienda_detail'),
]
