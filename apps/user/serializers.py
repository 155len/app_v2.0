from rest_framework import serializers
from .models import User, Couple
import random
import string

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']

class CoupleSerializer(serializers.ModelSerializer):
    user1_info = UserSerializer(source='user1', read_only=True)
    user2_info = UserSerializer(source='user2', read_only=True)
    
    class Meta:
        model = Couple
        fields = ['id', 'code', 'user1', 'user2', 'user1_info', 'user2_info', 'status', 'created_at']
        read_only_fields = ['id', 'code', 'created_at']

class WeChatLoginSerializer(serializers.Serializer):
    code = serializers.CharField()

class CreateCoupleSerializer(serializers.Serializer):
    pass

class JoinCoupleSerializer(serializers.Serializer):
    code = serializers.CharField()
