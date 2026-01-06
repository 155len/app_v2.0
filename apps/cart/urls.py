from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('items/', views.add_to_cart, name='add_to_cart'),
    path('items/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('items/<int:pk>/delete/', views.delete_cart_item, name='delete_cart_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
]
