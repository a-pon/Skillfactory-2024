from datetime import datetime, timezone

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect

from .models import Post


class PostLimitError(Exception):
    pass


@receiver(pre_save, sender=Post)
def limit_daily_posts(sender, instance, **kwargs):
    if not Post.objects.filter(id=instance.id).exists():
        posts = Post.objects.filter(
            author=instance.author,
            time__gte=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
        )
        if posts.count() >= 3:
            raise PostLimitError('Daily posts limit achieved')


@receiver(post_save, sender=Post)
def notify_category_subscribers(sender, instance, created, **kwargs):
    if created:
        instance.categories.add(instance._categories)
        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                html_content = render_to_string(
                    'post_created.html',
                    {
                        'post': instance,
                        'subscriber': subscriber,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=instance.header,
                    body=instance.content,
                    from_email='',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
