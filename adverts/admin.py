from django.contrib import admin

from adverts.models import Advertisement


# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'created')
    readonly_fields = ('views',)
    search_fields = ('title', 'category')
