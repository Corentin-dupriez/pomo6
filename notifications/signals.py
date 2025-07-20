from django.contrib.auth import get_user_model
from django.db.models import signals, Q
from django.dispatch import receiver

from adverts import models
from chat.models import Message
from notifications.utils import notify

UserModel = get_user_model()


@receiver(signals.post_save, sender=models.Advertisement)
def create_advertisement(sender, instance: models.Advertisement, created, **kwargs) -> None:
    if created:
        return
    if not created and instance.approved:
        notify(target_user=instance.user,
               text=f'Your advertisement "{instance.title}" has been approved.',
               target_url=instance.get_absolute_url())


@receiver(signals.post_save, sender=Message)
def create_message(sender, instance: Message, created, **kwargs) -> None:
    if created:
        recipient = instance.thread.participants.exclude(pk=instance.sender.pk).first()
        if recipient:
            notify(
                target_user=recipient,
                text=f'{instance.sender} has sent you a message',
                target_url=instance.thread.get_absolute_url()
            )