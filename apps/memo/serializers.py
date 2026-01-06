from rest_framework import serializers
from .models import Memo, MemoItem

class MemoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoItem
        fields = ['id', 'content', 'is_completed', 'sort_order', 'created_at', 'completed_at']
        read_only_fields = ['id', 'created_at', 'completed_at']

class MemoSerializer(serializers.ModelSerializer):
    items_count = serializers.ReadOnlyField()
    completed_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Memo
        fields = ['id', 'title', 'user', 'couple', 'is_shared', 'items_count', 'completed_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'couple', 'created_at', 'updated_at']

class MemoDetailSerializer(serializers.ModelSerializer):
    items = MemoItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Memo
        fields = ['id', 'title', 'user', 'couple', 'is_shared', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
