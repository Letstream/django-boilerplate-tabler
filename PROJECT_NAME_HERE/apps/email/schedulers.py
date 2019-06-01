from apps.core.utils import getOption
from .tasks import email_task, execute_email_task
from .models import Email, EmailQueue
from django.conf import settings

def ScheduleEmail(to_email, subject, html_text, plain_text, from_email=None):
    try:
        email = Email.objects.create(
            from_email = from_email if from_email != None else getOption('send_mails_as'),
            to_email=to_email,
            subject=subject,
            html_text=html_text,
            plain_text=plain_text
        )

        task = EmailQueue.objects.create(email=email)
        if not settings.USE_CELERY:
            execute_email_task(task.id)
        else:
            email_task.delay(task.id)
        
        return True
    except Exception as e:
        raise