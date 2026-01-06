from django.contrib import admin
from .models import User, Couple

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'openid', 'created_at']
    search_fields = ['username', 'nickname', 'openid']

@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'user1', 'user2', 'status', 'created_at']
    search_fields = ['code']
