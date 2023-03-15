import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MBoard.settings')

app = Celery('MBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_onetimecodes_older_5_minutes_every_1_minute': {
        'task': 'board.tasks.delete_more_5m_codes',
        'schedule': crontab(),
    },
}
