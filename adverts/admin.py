from django.contrib import admin

from adverts.models import Advertisement


# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created')
    search_fields = ('title', 'category')
