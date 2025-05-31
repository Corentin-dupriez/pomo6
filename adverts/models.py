from django.db import models
from django.utils.text import slugify


# Create your models here.
class Advertisement(models.Model):
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
    created = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100,
                                choices=CategoryChoices.choices,
                                default=CategoryChoices.OTHER)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increase_views(self):
        self.views += 1

    def __str__(self):
        return self.title
