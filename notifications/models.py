from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class Notification(models.Model):
    target_user = models.ForeignKey(UserModel,
                                    on_delete=models.CASCADE)

    text = models.TextField()

    read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    url = models.URLField()

    def __str__(self):
        return self.text

    def mark_as_read(self):
        self.read = True
        self.save()
