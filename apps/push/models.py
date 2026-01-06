from django.db import models
from apps.user.models import User

class PushTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_tasks', verbose_name='接收用户')
    template_id = models.CharField(max_length=100, verbose_name='模板ID')
    title = models.CharField(max_length=100, verbose_name='推送标题')
    content = models.TextField(verbose_name='推送内容')
    push_time = models.DateTimeField(verbose_name='推送时间')
    is_sent = models.BooleanField(default=False, verbose_name='是否已推送')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='实际推送时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'push_task'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.title} - {self.push_time}'

class PushLog(models.Model):
    task = models.ForeignKey(PushTask, on_delete=models.CASCADE, related_name='logs', verbose_name='推送任务')
    status = models.CharField(max_length=20, choices=[
        ('success', '成功'),
        ('failed', '失败')
    ], verbose_name='状态')
    error_message = models.TextField(blank=True, verbose_name='错误信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'push_log'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.task.title} - {self.status}'
