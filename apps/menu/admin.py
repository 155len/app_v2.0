from django.contrib import admin
from .models import MenuCategory, MenuItem

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sort_order', 'couple', 'created_at']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'is_available', 'created_at']
    search_fields = ['name']
    list_filter = ['is_available', 'category']
