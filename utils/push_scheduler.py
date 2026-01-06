from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from apps.push.models import PushTask, PushLog
from apps.push.services import WeChatPushService

scheduler = BackgroundScheduler()

def send_push_notification():
    pending_tasks = PushTask.objects.filter(
        is_sent=False,
        push_time__lte=timezone.now()
    )
    
    for task in pending_tasks:
        try:
            service = WeChatPushService()
            result = service.send_message(
                openid=task.user.openid,
                template_id=task.template_id,
                data={
                    'title': {'value': task.title},
                    'content': {'value': task.content}
                }
            )
            
            if result.get('errcode') == 0:
                task.is_sent = True
                task.sent_at = timezone.now()
                task.save()
                
                PushLog.objects.create(
                    task=task,
                    status='success'
                )
            else:
                PushLog.objects.create(
                    task=task,
                    status='failed',
                    error_message=result.get('errmsg', 'Unknown error')
                )
        except Exception as e:
            PushLog.objects.create(
                task=task,
                status='failed',
                error_message=str(e)
            )

def start_scheduler():
    scheduler.add_job(
        send_push_notification,
        'interval',
        minutes=1,
        id='push_notification'
    )
    scheduler.start()
