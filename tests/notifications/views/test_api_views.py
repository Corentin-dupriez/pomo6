from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notifications.models import Notification

UserModel = get_user_model()

class TestNotificationAPIView(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        self.notification = Notification.objects.create(
            target_user=self.user,
            text="test",
        )
        self.client.login(username="testuser", password="<PASSWORD>")

    def test__read_notification_by_user__marks_as_read(self):
        self.assertFalse(self.notification.read)
        response = self.client.patch(reverse('read-notification',
                                  kwargs={'pk': self.notification.id}),
                          data={'read': True})
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__read_notification_by_other_user__returns_403(self):
        user2 = UserModel.objects.create_user(
            username="otheruser",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        self.client.login(username="otheruser", password="<PASSWORD>")
        response = self.client.patch(reverse('read-notification',
                                  kwargs={'pk': self.notification.id}),
                          data={'read': True})
        self.notification.refresh_from_db()
        self.assertFalse(self.notification.read)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)