from django.dispatch import receiver
from common.tasks import send_email
from adverts.models import Advertisement, Order
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

@receiver(signals.post_save, sender=Order)
def send_email_to_user(sender, instance: Order, created, **kwargs):
    if created:
            send_email.delay(
                subject='New order created',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=instance.user.email,
                action='order-created',
                context={
                    'username': instance.user.username,
                    'seller': instance.advertisement.user.username,
                    'listing': str(instance.advertisement)
                }
            )
    else:
        if instance.status == 'APPROVED':
            send_email.delay(
                subject='Order approved',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=instance.advertisement.user.email,
                action='order-approved',
                context={
                    'username': instance.advertisement.user.username,
                    'client': instance.user.username,
                    'listing': str(instance.advertisement)
                }
            )
        elif instance.status == 'COMPLETED':
            send_email.delay(
                subject='Order completed',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=instance.user.email,
                action='order-completed',
                context={
                    'username': instance.user.username,
                    'seller': instance.advertisement.user.username,
                    'listing': str(instance.advertisement)
                }
            )