from datetime import datetime, timedelta, timezone

from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Category, Post


@shared_task
def email_subscribers():
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
