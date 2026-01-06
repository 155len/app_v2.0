from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Memo, MemoItem
from .serializers import MemoSerializer, MemoDetailSerializer, MemoItemSerializer
from apps.user.models import Couple

def get_user_couple(user):
    try:
        return Couple.objects.get(user1=user)
    except Couple.DoesNotExist:
        try:
            return Couple.objects.get(user2=user)
        except Couple.DoesNotExist:
            return None

@api_view(['GET', 'POST'])
def memos(request):
    if request.method == 'GET':
        couple = get_user_couple(request.user)
        if couple:
            memos = Memo.objects.filter(couple=couple)
        else:
            # 未绑定情侣关系的用户返回自己的备忘录
            memos = Memo.objects.filter(user=request.user, couple__isnull=True)
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        couple = get_user_couple(request.user)
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, couple=couple)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def memo_detail(request, pk):
    couple = get_user_couple(request.user)
    
    try:
        if couple:
            memo = Memo.objects.get(pk=pk, couple=couple)
        else:
            memo = Memo.objects.get(pk=pk, user=request.user, couple__isnull=True)
    except Memo.DoesNotExist:
        return Response({'error': '备忘录不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MemoDetailSerializer(memo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MemoSerializer(memo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        memo.delete()
        return Response({'success': True})

@api_view(['POST'])
def add_memo_item(request, pk):
    couple = get_user_couple(request.user)
    
    try:
        if couple:
            memo = Memo.objects.get(pk=pk, couple=couple)
        else:
            memo = Memo.objects.get(pk=pk, user=request.user, couple__isnull=True)
    except Memo.DoesNotExist:
        return Response({'error': '备忘录不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MemoItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(memo=memo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def memo_item_detail(request, pk, item_id):
    couple = get_user_couple(request.user)
    
    try:
        if couple:
            memo = Memo.objects.get(pk=pk, couple=couple)
        else:
            memo = Memo.objects.get(pk=pk, user=request.user, couple__isnull=True)
        item = MemoItem.objects.get(pk=item_id, memo=memo)
    except (Memo.DoesNotExist, MemoItem.DoesNotExist):
        return Response({'error': '备忘录或事项不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = MemoItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            is_completed = serializer.validated_data.get('is_completed')
            if is_completed and not item.is_completed:
                from django.utils import timezone
                serializer.validated_data['completed_at'] = timezone.now()
            elif not is_completed:
                serializer.validated_data['completed_at'] = None
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return Response({'success': True})
