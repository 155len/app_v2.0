from django.urls import path
from . import views

urlpatterns = [
    path('wechat-login/', views.wechat_login, name='wechat_login'),
    path('user-info/', views.user_info, name='user_info'),
    path('create-couple/', views.create_couple, name='create_couple'),
    path('join-couple/', views.join_couple, name='join_couple'),
]
