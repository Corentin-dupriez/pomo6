from cloudinary import CloudinaryResource
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomImageFormatValidator:
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self, value):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            value = 'Incorrect image format'
        self.__message = value

    def __call__(self, value: CloudinaryResource|InMemoryUploadedFile):
        if isinstance(value, CloudinaryResource):
            if value.format not in ['png', 'jpg', 'jpeg', 'webp']:
                raise ValidationError(message=self.message)
        elif isinstance(value, InMemoryUploadedFile):
            name = value.name.lower()
            extension = name.split('.')[-1]
            if extension not in ['png', 'jpg', 'jpeg', 'webp']:
                raise ValidationError(message=self.message)