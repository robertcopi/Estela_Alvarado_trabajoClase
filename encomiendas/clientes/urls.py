from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='cliente_list'),
    path('nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
]
