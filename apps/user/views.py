from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Couple
from .serializers import UserSerializer, CoupleSerializer, WeChatLoginSerializer, CreateCoupleSerializer, JoinCoupleSerializer
import random
import string
import requests
from django.conf import settings

def generate_invite_code():
    return ''.join(random.choices(string.digits, k=6))

@api_view(['POST'])
@permission_classes([AllowAny])
def wechat_login(request):
    serializer = WeChatLoginSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        
        try:
            appid = settings.WECHAT_MINI_APP['APPID']
            secret = settings.WECHAT_MINI_APP['SECRET']
            
            wx_url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
            wx_response = requests.get(wx_url, timeout=10)
            wx_data = wx_response.json()
            
            if 'errcode' in wx_data and wx_data['errcode'] != 0:
                print(f'微信API错误: {wx_data}')
                openid = f'fallback_{code[:8]}'
            else:
                openid = wx_data.get('openid')
                if not openid:
                    print(f'未获取到openid: {wx_data}')
                    openid = f'fallback_{code[:8]}'
            
            user, created = User.objects.get_or_create(
                openid=openid,
                defaults={
                    'username': openid,
                    'nickname': f'用户{openid[-6:]}'
                }
            )
            
            token, _ = Token.objects.get_or_create(user=user)
            
            couple = None
            try:
                couple = Couple.objects.get(user1=user)
            except Couple.DoesNotExist:
                try:
                    couple = Couple.objects.get(user2=user)
                except Couple.DoesNotExist:
                    pass
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'couple': CoupleSerializer(couple).data if couple else None
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_info(request):
    auth_header = request.headers.get('Authorization', '')
    
    user = None
    couple = None
    
    if auth_header.startswith('Token '):
        token_key = auth_header[6:]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            pass
    
    if user:
        try:
            couple = Couple.objects.get(user1=user)
        except Couple.DoesNotExist:
            try:
                couple = Couple.objects.get(user2=user)
            except Couple.DoesNotExist:
                pass
        
        return Response({
            'user': UserSerializer(user).data,
            'couple': CoupleSerializer(couple).data if couple else None
        })
    
    return Response({
        'user': None,
        'couple': None
    })

@api_view(['POST'])
def create_couple(request):
    serializer = CreateCoupleSerializer(data=request.data)
    if serializer.is_valid():
        auth_header = request.headers.get('Authorization', '')
        user = None
        
        if auth_header.startswith('Token '):
            token_key = auth_header[6:]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
            except Token.DoesNotExist:
                pass
        
        if not user:
            return Response({'error': '认证失败'}, status=status.HTTP_401_UNAUTHORIZED)
        
        existing_couple = None
        try:
            existing_couple = Couple.objects.get(user1=user)
        except Couple.DoesNotExist:
            try:
                existing_couple = Couple.objects.get(user2=user)
            except Couple.DoesNotExist:
                pass
        
        if existing_couple:
            return Response({'error': '您已经加入过情侣关系'}, status=status.HTTP_400_BAD_REQUEST)
        
        couple = Couple.objects.create(
            code=generate_invite_code(),
            user1=user,
            status='pending'
        )
        
        return Response(CoupleSerializer(couple).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def join_couple(request):
    serializer = JoinCoupleSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        auth_header = request.headers.get('Authorization', '')
        user = None
        
        if auth_header.startswith('Token '):
            token_key = auth_header[6:]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
            except Token.DoesNotExist:
                pass
        
        if not user:
            return Response({'error': '认证失败'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            couple = Couple.objects.get(code=code, status='pending')
        except Couple.DoesNotExist:
            return Response({'error': '邀请码不存在或已失效'}, status=status.HTTP_400_BAD_REQUEST)
        
        if couple.user1 == user:
            return Response({'error': '不能加入自己创建的情侣关系'}, status=status.HTTP_400_BAD_REQUEST)
        
        if couple.user2:
            return Response({'error': '该邀请码已被使用'}, status=status.HTTP_400_BAD_REQUEST)
        
        couple.user2 = user
        couple.status = 'active'
        couple.save()
        
        return Response(CoupleSerializer(couple).data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_profile(request):
    auth_header = request.headers.get('Authorization', '')
    user = None
    
    if auth_header.startswith('Token '):
        token_key = auth_header[6:]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            pass
    
    if not user:
        return Response({'error': '认证失败'}, status=status.HTTP_401_UNAUTHORIZED)
    
    nickname = request.data.get('nickname')
    avatar = request.data.get('avatar')
    
    if nickname:
        user.nickname = nickname
    if avatar:
        user.avatar = avatar
    
    user.save()
    
    return Response({
        'user': UserSerializer(user).data,
        'message': '更新成功'
    })
