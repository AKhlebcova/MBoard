from celery import shared_task
from .models import OnetimeCode
from datetime import datetime, timedelta


@shared_task
def delete_more_5m_codes():
    more_5_minutes = OnetimeCode.objects.filter(create_date__lte=datetime.now() - timedelta(minutes=5)).all()
    more_5_minutes.delete()
