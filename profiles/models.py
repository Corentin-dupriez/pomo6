from cloudinary import CloudinaryResource
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model
from common.tasks import convert_image_task
from cloudinary.models import CloudinaryField

from common.validators import CustomImageFormatValidator

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

    image = CloudinaryField(blank=True,
                              null=True,
                              max_length=500,
                              validators=[CustomImageFormatValidator()])

    def save(self, *args, **kwargs):
        if self.image:
            if isinstance(self, CloudinaryResource):
                if self.image.format != 'webp':
                    convert_image_task.delay(self._meta.app_label,
                                             self.__class__.__name__,
                                             self.user_id, 'image')
            elif isinstance(self, InMemoryUploadedFile):
                if not self.name.endswith('.webp'):
                    convert_image_task.delay(self._meta.app_label,
                                             self.__class__.__name__,
                                             self.user_id, 'image')

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username

    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name or self.user.username