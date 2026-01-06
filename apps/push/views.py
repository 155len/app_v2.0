from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PushTask, PushLog
from .serializers import PushTaskSerializer, PushLogSerializer
from django.utils import timezone

@api_view(['GET', 'POST'])
def push_tasks(request):
    if request.method == 'GET':
        tasks = PushTask.objects.filter(user=request.user)
        serializer = PushTaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PushTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def push_task_detail(request, pk):
    try:
        task = PushTask.objects.get(pk=pk, user=request.user)
        task.delete()
        return Response({'success': True})
    except PushTask.DoesNotExist:
        return Response({'error': '推送任务不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def push_logs(request):
    logs = PushLog.objects.filter(task__user=request.user)
    serializer = PushLogSerializer(logs, many=True)
    return Response(serializer.data)
