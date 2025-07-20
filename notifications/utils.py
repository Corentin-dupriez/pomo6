from django.contrib.auth import get_user_model

from .models import Notification

UserModel = get_user_model()

def notify(target_user: UserModel, text: str, target_url: str):
    notif = Notification.objects.create(
        target_user=target_user,
        text=text,
        url=target_url
    )
    notif.save()