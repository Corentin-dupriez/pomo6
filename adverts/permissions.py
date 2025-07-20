from rest_framework import permissions

from adverts.models import Order


class IsOrderOwnerOrClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Order):
        return obj.user == request.user or obj.advertisement.user == request.user
