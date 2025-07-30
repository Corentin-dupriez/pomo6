from django.contrib.auth import get_user_model
from django.test import TestCase

from notifications.models import Notification

UserModel = get_user_model()

class OrderModelTestCase(TestCase):
    def setUp(self):
        #arrange
        self.user = UserModel.objects.create_user(username='test',
                                                  email='test@test.com',
                                                  password='12test34')
        #act
        self.notification = Notification.objects.create(target_user=self.user,
                                                        text='Test notification',
                                                        url='https://test.com',
                                                        )

    def test__notification_creations__initiates_default_values(self):
        self.assertFalse(self.notification.read)

    def test__mark_as_read_function__marks_notification_as_read(self):
        #act
        self.notification.mark_as_read()
        #assert
        self.assertTrue(self.notification.read)

    def test__str_notification__returns_text(self):
        self.assertEqual(self.notification.__str__(), self.notification.text)