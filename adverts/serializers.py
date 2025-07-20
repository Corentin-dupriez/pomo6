from rest_framework import serializers

from adverts.models import Order, Advertisement


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class ListingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['approved']