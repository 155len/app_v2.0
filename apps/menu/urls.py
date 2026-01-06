from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('items/', views.items, name='items'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('upload/', views.upload_image, name='upload_image'),
]
