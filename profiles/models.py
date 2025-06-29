from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE)
    description = models.TextField(blank=True,
                                   null=True)
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to='profiles/images')

    def __str__(self):
        return self.user.username