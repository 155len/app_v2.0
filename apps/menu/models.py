from django.db import models
from django.conf import settings
from apps.user.models import Couple

class MenuCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名称')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    icon = models.CharField(max_length=100, blank=True, verbose_name='图标')
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属情侣')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'menu_category'
        ordering = ['sort_order']
        
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name='商品名称')
    description = models.TextField(blank=True, verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    image = models.URLField(blank=True, verbose_name='商品图片')
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items', verbose_name='所属分类')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_available = models.BooleanField(default=True, verbose_name='是否上架')
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属情侣')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'menu_item'
        ordering = ['sort_order']
        
    def __str__(self):
        return self.name
