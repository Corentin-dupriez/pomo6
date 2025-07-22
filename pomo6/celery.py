import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pomo6.settings')
app = Celery('pomo6')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()