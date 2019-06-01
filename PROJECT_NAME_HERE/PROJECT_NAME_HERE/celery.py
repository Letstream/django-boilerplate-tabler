import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT_NAME_HERE.settings')

app =  Celery('PROJECT_NAME_HERE')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()