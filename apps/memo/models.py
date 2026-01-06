from django.db import models
from apps.user.models import User, Couple

class Memo(models.Model):
    title = models.CharField(max_length=100, verbose_name='备忘录标题')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memos', verbose_name='创建用户')
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属情侣')
    is_shared = models.BooleanField(default=True, verbose_name='是否共享给伴侣')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'memo'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def items_count(self):
        return self.items.count()
    
    @property
    def completed_count(self):
        return self.items.filter(is_completed=True).count()

class MemoItem(models.Model):
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='items', verbose_name='所属备忘录')
    content = models.CharField(max_length=200, verbose_name='事项内容')
    is_completed = models.BooleanField(default=False, verbose_name='是否完成')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        db_table = 'memo_item'
        ordering = ['sort_order', 'created_at']
        
    def __str__(self):
        return self.content
