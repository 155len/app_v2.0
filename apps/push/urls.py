from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.push_tasks, name='push_tasks'),
    path('tasks/<int:pk>/', views.push_task_detail, name='push_task_detail'),
    path('logs/', views.push_logs, name='push_logs'),
]
