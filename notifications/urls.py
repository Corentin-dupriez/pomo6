from django.urls import path, include

from notifications.views import NotificationListView, ReadNotificationView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('api/', include([
        path('<int:pk>/read/', ReadNotificationView.as_view(), name='read-notification'),
    ]))
]