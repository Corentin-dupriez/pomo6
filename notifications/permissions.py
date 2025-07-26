from rest_framework import permissions


class IsNotificationRecipient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.target_user_id