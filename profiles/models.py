import io
import os
from PIL import Image
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserProfile(models.Model):
    #Profile created by a signal every time a new user registers
    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                primary_key=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    description = models.TextField(blank=True,
                                   null=True)

    image = models.ImageField(blank=True,
                              null=True,
                              upload_to='images/',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])])

    def save(self, *args, **kwargs):
        if self.image and self.image.name.split('.')[-1] != 'webp':
            image = Image.open(self.image)
            image = image.convert('RGB')

            buffer = io.BytesIO()
            image.save(buffer, format='webp')
            filename = os.path.splitext(self.image.name)[0] + '.webp'

            self.image.save(filename, ContentFile(buffer.getvalue()), save=False)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username

    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name or self.user.username