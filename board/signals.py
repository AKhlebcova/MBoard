from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Post, Feedback

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Feedback)
def feed_created_or_changed(sender, instance, created, **kwargs):
    instance.post.get_author()
    if created:
        subject = f'Новое сообщение от {instance.get_feedmaster()}'
        email = instance.post.author.email
        post_title = instance.post.title
        context = {
            'title': post_title,
            'instance': instance,
        }
        html_content = render_to_string(
            'add_new_feed.html',
            context=context,
        )
    else:
        subject = f'Ваше сообщение от {instance.get_message_date()} принято {instance.post.get_author()}'
        email = instance.user.email
        author = instance.post.get_author
        context = {
            'author': author,
            'instance': instance,
        }
        html_content = render_to_string(
            'feed_accepted.html',
            context=context,
        )

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='annakhlebtsova@yandex.ru',
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
