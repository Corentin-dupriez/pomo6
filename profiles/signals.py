from pomo6 import settings
from .models import UserProfile
from common.tasks import send_email
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.dispatch import receiver

UserModel = get_user_model()

@receiver(signals.post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs) -> None:
    if created:
        UserProfile.objects.create(user=instance)
        send_email.delay(subject=f'Welcome {instance.username}!',
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         to_email=instance.email,
                         action='welcome',
                         context={'user_pk': instance.pk})