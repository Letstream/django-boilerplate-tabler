from celery import shared_task
from .utils import send_mail
from .models import EmailQueue

@shared_task(bind=True)
def email_task(self, task_id):
    try:
        execute_email_task(task_id)
    except Exception as e:
        raise self.retry(exc=e, max_retries=3)

def execute_email_task(task_id):
    
    try:
        task = EmailQueue.objects.get(pk=task_id)
    except EmailQueue.DoesNotExist:
        return

    if task.status == "sent" or task.status == "sending":
        return

    # Update status
    task.status = "sending"
    task.save()
    
    # Send Mail
    try:
        send_mail(task.email)
    except Exception as e:
        task.status = "failed"
        task.save()
        raise

    # Update Status
    task.status = "sent"
    task.save()

    return True
