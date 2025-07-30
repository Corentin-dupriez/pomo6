from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.views.generic import ListView
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from notifications.permissions import IsNotificationRecipient


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notifications/my-notifications.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        return Notification.objects.filter(Q(target_user=self.request.user) &
                                           Q(read=False))


class ReadNotificationView(UpdateAPIView):
    queryset = Notification.objects.all()
    model = Notification
    serializer_class = NotificationSerializer
    permission_classes = (IsNotificationRecipient,)
    http_method_names = ['patch']

    def patch(self, request, **kwargs) -> Response:
        notif = self.get_object()
        serializer = self.get_serializer(instance=notif,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'success'},
                        status=status.HTTP_200_OK)