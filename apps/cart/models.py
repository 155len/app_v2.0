from django.db import models
from apps.user.models import User
from apps.menu.models import MenuItem

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='所属用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'cart'
        
    def __str__(self):
        return f'{self.user.nickname}的购物车'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='所属购物车')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        db_table = 'cart_item'
        unique_together = ['cart', 'item']
        
    def __str__(self):
        return f'{self.item.name} x {self.quantity}'
