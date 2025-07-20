from django.contrib import admin

from adverts.models import Advertisement, Order, Ratings, RatingResponse


# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created')
    search_fields = ('title', 'category')
    list_filter = ('approved', 'archived', 'category')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement', 'status', 'created')
    search_fields = ('user', 'advertisement')
    list_filter = ('status',)

@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    def order_user(self, obj: Ratings):
        return obj.order.advertisement.user

    list_display = ('order', 'rating', 'order_user', 'created')
    search_fields = ('order', 'rating')

@admin.register(RatingResponse)
class RatingResponseAdmin(admin.ModelAdmin):
    list_display = ('to_rating_id', 'comment' )