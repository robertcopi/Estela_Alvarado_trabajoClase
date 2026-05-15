from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('encomiendas/', views.encomiendas_list, name='encomiendas_list'),
    path('encomiendas/<int:pk>/', views.encomienda_detail, name='encomienda_detail'),
    path('encomiendas/<int:pk>/estado/', views.cambiar_estado, name='cambiar_estado'),
    path('encomiendas/nueva/', views.EncomiendaCreateView.as_view(), name='encomienda_create'),
    path('dashboard-rt/', views.dashboard_rt, name='dashboard_rt'),
]
