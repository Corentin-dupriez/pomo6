from django.contrib.auth import get_user_model
from django.test import TestCase
from adverts.models import Advertisement
from chat.models import Message, Thread
from notifications.models import Notification

UserModel = get_user_model()


class TestNotificationSignals(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='test',
            email='<EMAIL>',
            password='<PASSWORD>',
        )
        self.advertisement = Advertisement.objects.create(
            title='Test Advertisement',
            description='Test description',
            category=Advertisement.CategoryChoices.IT_HELP,
            fixed_price=100,
            user=self.user,
        )
        self.user2 = UserModel.objects.create_user(
            username='test2',
            email='<EMAIL>',
            password='<PASSWORD>',
        )
        self.thread = Thread.objects.create(
            advert=self.advertisement,
        )
        self.thread.participants.add(self.user, self.user2)

    def test__approve_advert__notifies_user(self):
        self.advertisement.refresh_from_db()
        self.advertisement.approve_listings()
        notifications = Notification.objects.filter(target_user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications.first().text, f'Your advertisement "{self.advertisement.title}" has been approved.')
        self.assertEqual(notifications.first().url, self.advertisement.get_absolute_url())

    def test__message__notifies_recipient(self):
        message = Message.objects.create(
            thread=self.thread,
            sender=self.user,
            content='Test content',
        )
        notifications = Notification.objects.filter(target_user=self.user2)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(Notification.objects.filter(target_user=self.user).count(), 0)
        self.assertEqual(notifications.first().text, f'{self.user.username} has sent you a message')
        self.assertEqual(notifications.first().url, self.thread.get_absolute_url())