from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')

app = Celery('parking_system')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-reminder-emails': {
        'task': 'reservations.tasks.send_reminder_emails',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
}
