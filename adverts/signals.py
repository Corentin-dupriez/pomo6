from django.dispatch import receiver
from common.tasks import send_email
from adverts.models import Advertisement
from pomo6 import settings
from django.db.models import signals


@receiver(signals.post_save, sender=Advertisement)
def send_email_to_user(sender, instance: Advertisement, created, **kwargs):
    if not created:
        if instance.approved:
            send_email.delay(
                subject='Advertisement Approved',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=instance.user.email,
                action='listing-approved',
                context={
                    'username': instance.user.username,
                    'listing': str(instance)
                }
            )
