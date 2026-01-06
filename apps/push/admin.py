from django.contrib import admin
from .models import PushTask, PushLog

@admin.register(PushTask)
class PushTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'push_time', 'is_sent', 'created_at']
    search_fields = ['title']
    list_filter = ['is_sent']

@admin.register(PushLog)
class PushLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'status', 'created_at']
    list_filter = ['status']
