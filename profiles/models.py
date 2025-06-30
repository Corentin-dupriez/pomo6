from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserProfile(models.Model):
    #Profile created by a signal every time a new user registers
    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE,
                                related_name='profile',)

    description = models.TextField(blank=True,
                                   null=True)

    image = models.ImageField(blank=True,
                              null=True,
                              upload_to='images/',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def __str__(self) -> str:
        return self.user.username