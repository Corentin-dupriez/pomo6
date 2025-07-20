import io
import os.path
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from adverts.mixins import CreatedDateMixin
from adverts.validators import RatingValidator

UserModel = get_user_model()


class Advertisement(CreatedDateMixin):

    class CategoryChoices(models.TextChoices):
        IT_HELP = ('IT', 'IT Help')
        HANDYMAN = ('HANDYMAN', 'Handyman')
        CLEANING = ('CLEANING', 'Cleaning')
        CHILDCARE = ('CHILDCARE', 'Childcare')
        TUTORING = ('TUTORING', 'Tutoring')
        PET_CARE = ('PET', 'Pet care')


    title = models.CharField(max_length=100)

    description = models.TextField(max_length=2000)

    category = models.CharField(max_length=100,
                                choices=CategoryChoices.choices,)

    slug = models.SlugField(blank=True,
                            max_length=200,)

    image = models.ImageField(upload_to='images/',
                              blank=True,
                              null=True,
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])])

    is_fixed_price = models.BooleanField(default=True)

    fixed_price = models.FloatField(blank=True,
                                    null=True)

    min_price = models.FloatField(blank=True,
                                  null=True)

    max_price = models.FloatField(blank=True,
                                  null=True)

    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE,
                             related_name='advertisements',)

    approved = models.BooleanField(default=False)

    archived = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('approve_listing', 'Can approve listing'),
        ]
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)

        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')
            buffer = io.BytesIO()
            img.save(buffer, format='webp')
            filename = os.path.splitext(self.image.name)[0] + '.webp'
            self.image.save(filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def increase_views(self) -> None:
        Views.objects.create(advertisement=self, view_date=timezone.now())

    def approve_listings(self) -> None:
        self.approved = True

    def get_absolute_url(self) -> str:
        return reverse('advert_view', kwargs={'pk': self.pk,
                                              'slug': self.slug})

    def __str__(self) -> str:
        return self.title

class Order(CreatedDateMixin):
    class StatusChoices(models.TextChoices):
        CREATED = ('CREATED', 'Created')
        SUBMITTED = ('SUBMITTED', 'Submitted')
        APPROVED = ('APPROVED', 'Approved')
        REJECTED = ('REJECTED', 'Rejected')
        PROCESSING = ('PROCESSING', 'Processing')
        COMPLETED = ('COMPLETED', 'Completed')

    advertisement = models.ForeignKey(to='Advertisement',
                                      on_delete=models.CASCADE,
                                      related_name='orders',)
    #orders are created through a thread,
    thread = models.ForeignKey(to='chat.Thread',
                               on_delete=models.CASCADE,
                               related_name='orders',)

    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE,
                             related_name='orders',)

    description = models.TextField(max_length=2000)

    last_modified = models.DateField(null=True,
                                     blank=True)

    accepted_on = models.DateField(null=True,
                                   blank=True)

    amount = models.FloatField(default=0)

    status = models.CharField(max_length=20,
                              choices=StatusChoices.choices,)

    completed_on = models.DateField(null=True,
                                    blank=True)

    def __str__(self) -> str:
        return f'Order for {self.advertisement} made on {self.created}'


class Ratings(CreatedDateMixin):
    class Meta:
        verbose_name_plural = 'Ratings'

    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='ratings')

    rating = models.DecimalField(decimal_places=1,
                                 max_digits=2,
                                 validators=[RatingValidator('The rating must be between 0 and 5')])

    comment = models.TextField(blank=True,
                               null=True)

class RatingResponse(CreatedDateMixin):
    to_rating = models.ForeignKey(Ratings,
                                  on_delete=models.CASCADE,
                                  related_name='responses')

    comment = models.TextField(blank=True,
                               null=True)

class Views(models.Model):
    view_date = models.DateTimeField(auto_now_add=True)

    advertisement = models.ForeignKey(Advertisement,
                                      on_delete=models.CASCADE,
                                      related_name='views')