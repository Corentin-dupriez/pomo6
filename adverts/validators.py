from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RatingValidator(object):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            value = 'The rating must be between 0 and 5'
        self.__message = value

    def __call__(self, value):
        if not 0 <= value <= 5:
            raise ValidationError(message=self.message)

@deconstructible
class FileExtensionValidator:
    def __init__(self, message:str=None) -> None:
        self.message = message
        self.allowed_extensions = ['png', 'jpg', 'jpeg']

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value or 'The file has to be a PNG or JPG'

    def __call__(self, value):
        if not value.split('.')[-1] in self.allowed_extensions:
            raise ValidationError(message=self.message)