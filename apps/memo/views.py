from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Memo, MemoItem
from .serializers import MemoSerializer, MemoDetailSerializer, MemoItemSerializer
from apps.user.models import Couple

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Token '):
        token_key = auth_header[6:]
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            pass
    return None

def get_user_couple(user):
    if not user:
        return None
    try:
        return Couple.objects.get(user1=user)
    except Couple.DoesNotExist:
        try:
            return Couple.objects.get(user2=user)
        except Couple.DoesNotExist:
            return None

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def memos(request):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    if request.method == 'GET':
        if couple:
            memos = Memo.objects.filter(couple=couple)
        else:
            memos = Memo.objects.filter(user=user, couple__isnull=True) if user else []
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        couple = get_user_couple(user)
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, couple=couple)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def memo_detail(request, pk):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    try:
        if couple:
            memo = Memo.objects.get(pk=pk, couple=couple)
        else:
            memo = Memo.objects.get(pk=pk, user=user, couple__isnull=True) if user else None
        if not memo:
            return Response({'error': '备忘录不存在'}, status=status.HTTP_404_NOT_FOUND)
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
@permission_classes([AllowAny])
def add_memo_item(request, pk):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    try:
        if couple:
            memo = Memo.objects.get(pk=pk, couple=couple)
        else:
            memo = Memo.objects.get(pk=pk, user=user, couple__isnull=True) if user else None
        if not memo:
            return Response({'error': '备忘录不存在'}, status=status.HTTP_404_NOT_FOUND)
    except Memo.DoesNotExist:
        return Response({'error': '备忘录不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MemoItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(memo=memo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([AllowAny])
def memo_item_detail(request, pk, item_id):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    try:
        if couple:
            memo = Memo.objects.get(pk=pk, couple=couple)
        else:
            memo = Memo.objects.get(pk=pk, user=user, couple__isnull=True) if user else None
        if not memo:
            return Response({'error': '备忘录不存在'}, status=status.HTTP_404_NOT_FOUND)
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
