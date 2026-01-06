from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer
from apps.user.models import Couple
import os
from django.conf import settings
import uuid

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
def categories(request):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    if request.method == 'GET':
        if couple:
            categories = MenuCategory.objects.filter(couple=couple)
        else:
            categories = MenuCategory.objects.filter(user=user) if user else []
        serializer = MenuCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        couple = get_user_couple(user)
        serializer = MenuCategorySerializer(data=request.data)
        if serializer.is_valid():
            if couple:
                serializer.save(couple=couple)
            elif user:
                serializer.save(user=user)
            else:
                return Response({'error': '需要登录'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def category_detail(request, pk):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    try:
        if couple:
            category = MenuCategory.objects.get(pk=pk, couple=couple)
        elif user:
            category = MenuCategory.objects.get(pk=pk, user=user)
        else:
            return Response({'error': '分类不存在'}, status=status.HTTP_404_NOT_FOUND)
    except MenuCategory.DoesNotExist:
        return Response({'error': '分类不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MenuCategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MenuCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response({'success': True})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def items(request):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    if request.method == 'GET':
        if couple:
            items = MenuItem.objects.filter(category__couple=couple)
        elif user:
            items = MenuItem.objects.filter(category__user=user)
        else:
            items = []
            
        category_id = request.query_params.get('category_id')
        keyword = request.query_params.get('keyword')
        
        if category_id:
            items = items.filter(category_id=category_id)
        
        if keyword:
            items = items.filter(name__icontains=keyword)
        
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        couple = get_user_couple(user)
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.validated_data['category']
            try:
                if couple:
                    MenuCategory.objects.get(pk=category.id, couple=couple)
                elif user:
                    MenuCategory.objects.get(pk=category.id, user=user)
                else:
                    return Response({'error': '需要登录'}, status=status.HTTP_401_UNAUTHORIZED)
                
                if couple:
                    serializer.save(category=category, couple=couple)
                elif user:
                    serializer.save(category=category, user=user)
                else:
                    serializer.save(category=category)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except MenuCategory.DoesNotExist:
                return Response({'error': '分类不存在'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def item_detail(request, pk):
    user = get_user_from_token(request)
    couple = get_user_couple(user)
    
    try:
        if couple:
            item = MenuItem.objects.get(pk=pk, category__couple=couple)
        elif user:
            item = MenuItem.objects.get(pk=pk, category__user=user)
        else:
            return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
    except MenuItem.DoesNotExist:
        return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            if 'category' in serializer.validated_data:
                category = serializer.validated_data['category']
                try:
                    if couple:
                        MenuCategory.objects.get(pk=category.id, couple=couple)
                    elif user:
                        MenuCategory.objects.get(pk=category.id, user=user)
                except MenuCategory.DoesNotExist:
                    return Response({'error': '分类不存在'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return Response({'success': True})

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_image(request):
    if 'image' not in request.FILES:
        return Response({'error': '没有上传文件'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    ext = os.path.splitext(image.name)[1]
    filename = f'{uuid.uuid4()}{ext}'
    
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    filepath = os.path.join(upload_dir, filename)
    with open(filepath, 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)
    
    url = f'{settings.MEDIA_URL}uploads/{filename}'
    return Response({'url': url}, status=status.HTTP_201_CREATED)
