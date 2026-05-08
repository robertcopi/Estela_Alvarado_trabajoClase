from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articulos/', views.articulos_list, name='articulos_list'),
    path('articulos/create/', views.articulo_create, name='articulo_create'),
    path('articulos/<uuid:articulo_id>/', views.articulo_detail, name='articulo_detail'),
    path('articulos/<uuid:articulo_id>/edit/', views.articulo_edit, name='articulo_edit'),
    
    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<uuid:articulo_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<uuid:articulo_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    
    # Checkout and Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/<uuid:pedido_id>/', views.order_detail, name='order_detail'),
    path('order/<uuid:pedido_id>/pdf/', views.generate_pdf_order, name='generate_pdf_order'),
    path('order/<uuid:pedido_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # API URLs
    path('api/articulos/', views.api_articulos, name='api_articulos'),
]
