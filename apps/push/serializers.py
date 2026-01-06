from rest_framework import serializers
from .models import PushTask, PushLog

class PushTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushTask
        fields = ['id', 'user', 'template_id', 'title', 'content', 'push_time', 'is_sent', 'sent_at', 'created_at']
        read_only_fields = ['id', 'user', 'is_sent', 'sent_at', 'created_at']

class PushLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushLog
        fields = ['id', 'task', 'status', 'error_message', 'created_at']
        read_only_fields = ['id', 'created_at']
