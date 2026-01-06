from rest_framework import serializers
from .models import MenuCategory, MenuItem

class MenuCategorySerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'sort_order', 'icon', 'items_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_items_count(self, obj):
        return obj.items.count()

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'category_name', 'sort_order', 'is_available', 'couple', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
