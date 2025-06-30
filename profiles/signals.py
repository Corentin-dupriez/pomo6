from .models import UserProfile

from django.db.models import signals
from django.contrib.auth import get_user_model
from django.dispatch import receiver

UserModel = get_user_model()

@receiver(signals.post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs) -> None:
    if created:
        UserProfile.objects.create(user=instance)