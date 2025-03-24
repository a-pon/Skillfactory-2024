import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('news', include=['news.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # 'email_every_monday': {
    #     'task': 'tasks.email_subscribers',
    #     'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    # },
}

app.autodiscover_tasks()
