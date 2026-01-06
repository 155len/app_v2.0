from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    openid = models.CharField(max_length=128, unique=True, verbose_name='微信OpenID')
    nickname = models.CharField(max_length=100, verbose_name='昵称')
    avatar = models.URLField(verbose_name='头像')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'user'
        
    def __str__(self):
        return self.nickname or self.username

class Couple(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='邀请码')
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='couple_as_user1', verbose_name='用户1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='couple_as_user2', null=True, blank=True, verbose_name='用户2')
    status = models.CharField(max_length=20, choices=[
        ('pending', '待确认'),
        ('active', '已绑定'),
        ('inactive', '已解绑')
    ], default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'couple'
        
    def __str__(self):
        return f'{self.user1.nickname} - {self.user2.nickname if self.user2 else "未绑定"}'
