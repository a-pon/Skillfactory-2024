from datetime import datetime, timedelta, timezone
import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from ...models import Advert

logger = logging.getLogger(__name__)


def weekly_newsletter_job():
    new_adverts = Advert.objects.filter(
        time__gt=datetime.now(timezone.utc)-timedelta(weeks=1),
    )
    if new_adverts:
        for user in User.objects.all():
            html_content = render_to_string(
                'notify/newsletter.html',
                {
                    'adverts': new_adverts,
                    'user': user,
                }
            )
            msg = EmailMultiAlternatives(
                subject='Новые объявления',
                body='',
                from_email='',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_newsletter_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="10", minute="00"
            ),
            id = "weekly_newsletter_job",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added weekly job 'weekly_newsletter_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
