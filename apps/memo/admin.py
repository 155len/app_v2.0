from django.contrib import admin
from .models import Memo, MemoItem

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'couple', 'is_shared', 'created_at']
    search_fields = ['title']
    list_filter = ['is_shared']

@admin.register(MemoItem)
class MemoItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'memo', 'is_completed', 'created_at']
    list_filter = ['is_completed']
