from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from notifications.models import Notification


# Create your views here.
class NotificationListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notifications/my-notifications.html'

    def get_queryset(self):
        return Notification.objects.filter(Q(target_user=self.request.user) &
                                           Q(read=False))