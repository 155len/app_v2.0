from django.urls import path
from . import views

urlpatterns = [
    path('', views.memos, name='memos'),
    path('<int:pk>/', views.memo_detail, name='memo_detail'),
    path('<int:pk>/items/', views.add_memo_item, name='add_memo_item'),
    path('<int:pk>/items/<int:item_id>/', views.memo_item_detail, name='memo_item_detail'),
]
