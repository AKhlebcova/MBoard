import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime, timedelta
from board.models import Post, User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def my_job():
    post_seven_days = Post.objects.filter(public_date__gte=datetime.now() - timedelta(days=7)).all()
    subject = f'На нашем сайте за прошедшую неделю появились новые объявления!'
    people_emails = list(User.objects.all().values_list('email', flat=True))
    html_content = render_to_string(
        'posts_7days.html',
        context={'posts': post_seven_days},
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body='posts',
        from_email='annakhlebtsova@yandex.ru',
        to=people_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            #  То же, что и интервал, но задача тригера таким образом более понятна django (second="*/10")
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
