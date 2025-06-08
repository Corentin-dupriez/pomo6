from django.db import models
from django.utils.text import slugify

from adverts.mixins import CreatedDateMixin
from adverts.validators import RatingValidator


# Create your models here.
class Advertisement(CreatedDateMixin):
    class CategoryChoices(models.TextChoices):
        IT_HELP = ('IT', 'IT Help')
        HANDYMAN = ('HANDYMAN', 'Handyman')
        CLEANING = ('CLEANING', 'Cleaning')
        CHILDCARE = ('CHILDCARE', 'Childcare')
        TUTORING = ('TUTORING', 'Tutoring')
        TRANSPORTATION = ('TRANSPORTATION', 'Transportation')
        PET_CARE = ('PET', 'Pet care')
        OTHER = ('OTHER', 'Other')


    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100,
                                choices=CategoryChoices.choices,
                                default=CategoryChoices.OTHER)
    slug = models.SlugField(blank=True)

    #TO-DO: WILL HAVE TO CHANGE MODEL TO FK ONCE USERS ARE IMPLEMENTED
    user = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increase_views(self):
        self.views += 1

    def __str__(self):
        return self.title


class Order(CreatedDateMixin):
    advertisement = models.ForeignKey(Advertisement,
                                      on_delete=models.CASCADE,
                                      related_name='orders',)
    #TO-DO: WILL HAVE TO CHANGE MODEL TO FK ONCE USERS ARE IMPLEMENTED
    user = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)


class Ratings(CreatedDateMixin):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='ratings')
    rating = models.DecimalField(decimal_places=1,
                                 max_digits=2,
                                 validators=[RatingValidator('The rating must be between 0 and 5')])
    comment = models.TextField(blank=True,
                               null=True)

    def __str__(self):
        return f'{self.user} - {self.rating}'