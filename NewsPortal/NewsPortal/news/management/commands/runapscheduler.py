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
from django.shortcuts import redirect

from ...models import Post, Category

logger = logging.getLogger(__name__)


def category_update_job():
    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            time__gt=datetime.now(timezone.utc)-timedelta(weeks=1),
            categories=category
        )
        if new_posts:
            for subscriber in category.subscribers.all():
                html_content = render_to_string(
                    'category_update.html',
                    {
                        'posts': new_posts,
                        'category': category,
                        'subscriber': subscriber,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject='Новые статьи',
                    body='',
                    from_email='',
                    to=[subscriber.email],
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
            category_update_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="10", minute="00"
            ),
            id = "category_update_job",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added job 'category_update_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
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
