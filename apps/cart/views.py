from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.menu.models import MenuItem

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

@api_view(['GET'])
@permission_classes([AllowAny])
def cart_detail(request):
    user = get_user_from_token(request)
    if not user:
        return Response({'items': [], 'total_price': 0, 'total_quantity': 0})
    
    cart, created = Cart.objects.get_or_create(user=user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart(request):
    user = get_user_from_token(request)
    if not user:
        return Response({'error': '需要登录'}, status=status.HTTP_401_UNAUTHORIZED)
    
    cart, _ = Cart.objects.get_or_create(user=user)
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        item = MenuItem.objects.get(pk=item_id)
    except MenuItem.DoesNotExist:
        return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_cart_item(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({'error': '需要登录'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        cart_item = CartItem.objects.get(pk=pk, cart__user=user)
    except CartItem.DoesNotExist:
        return Response({'error': '购物车项不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    quantity = request.data.get('quantity', cart_item.quantity)
    
    if quantity <= 0:
        cart_item.delete()
        return Response({'success': True})
    
    cart_item.quantity = quantity
    cart_item.save()
    
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_cart_item(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({'error': '需要登录'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        cart_item = CartItem.objects.get(pk=pk, cart__user=user)
        cart_item.delete()
        return Response({'success': True})
    except CartItem.DoesNotExist:
        return Response({'error': '购物车项不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_cart(request):
    user = get_user_from_token(request)
    if not user:
        return Response({'error': '需要登录'}, status=status.HTTP_401_UNAUTHORIZED)
    
    cart, _ = Cart.objects.get_or_create(user=user)
    cart.items.all().delete()
    return Response({'success': True})
