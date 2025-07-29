from django.contrib.auth import get_user_model
from django.test import TestCase
from adverts.models import Advertisement
from chat.models import Thread, Message
from chat.templatetags.last_message import last_message
from chat.templatetags.other_participant import other_participant

UserModel = get_user_model()

class OrderModelTestCase(TestCase):
    def setUp(self):
        #arrange
        self.user = UserModel.objects.create_user(username='test',
                                                  email='test@test.com',
                                                  password='12test34')
        self.user2 = UserModel.objects.create_user(username='test2',
                                                   email='test2.test.com',
                                                   password='<PASSWORD>')
        self.advertisement = Advertisement.objects.create(
            title='Test Advertisement',
            description='Test description',
            user=self.user,
            category=Advertisement.CategoryChoices.IT_HELP,
            fixed_price=100,
        )
        self.thread = Thread.objects.create(advert=self.advertisement)
        self.thread.participants.add(self.user,
                                     self.user2,)
        self.message1 = Message.objects.create(
            thread=self.thread,
            content='Test Message 1',
            sender=self.user,
        )
        self.message2 = Message.objects.create(
            thread=self.thread,
            content='Test Message 2',
            sender=self.user2,
        )

    def test__last_message_templatetag__returns_last_created_message(self):
        tag_result = last_message(self.thread)
        self.assertEqual(tag_result, self.message2)

    def test__other_participants_templatetag__returns_other_participants(self):
        tag_result = other_participant(self.thread, self.user.pk)
        self.assertEqual(tag_result, self.user2.pk)