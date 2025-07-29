from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from adverts.models import Advertisement
from chat.models import Thread

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
        #act
        self.thread = Thread.objects.create(advert=self.advertisement)
        self.thread.participants.add(self.user,
                                     self.user2,)

    def test__str_thread__returns_usernames_and_advertisement(self):
        #assert
        self.assertEqual(str(self.thread),
                         f'Thread between {' and '.join([user.get_username() for user in self.thread.participants.all()])} '
                                f'for {self.thread.advert.title}')

    def test__thread_get_absolute_url__returns_url(self):
        #assert
        self.assertEqual(str(self.thread.get_absolute_url()),
                         reverse('thread-detail', kwargs={'pk': self.thread.pk}))