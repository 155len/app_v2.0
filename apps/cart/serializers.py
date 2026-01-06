from rest_framework import serializers
from .models import Cart, CartItem
from apps.menu.serializers import MenuItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity', 'added_at']
        read_only_fields = ['id', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_quantity', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())
    
    def get_total_price(self, obj):
        return sum(item.item.price * item.quantity for item in obj.items.all())
