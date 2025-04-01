from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Respond


@receiver(post_save, sender=Respond)
def notify_advert_author(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
           'notify/respond_created.html',
           {
               'respond': instance,
               'advert_author': instance.advert.author,
           }
        )
        msg = EmailMultiAlternatives(
           subject=instance.advert.header,
           body=instance.content,
           from_email='',
           to=[instance.advert.author.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Respond)
def notify_respond_author(sender, instance, created, update_fields, **kwargs):
    if not created:
        if 'accepted' in update_fields:
            html_content = render_to_string(
                'notify/respond_accepted.html',
                {
                    'respond': instance,
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.advert.header,
                body=instance.content,
                from_email='',
                to=[instance.author.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
