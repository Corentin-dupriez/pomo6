from django.contrib.auth import get_user_model
from django.test import TestCase

from profiles.models import UserProfile

UserModel = get_user_model()

class OrderModelTestCase(TestCase):
    def setUp(self):
        #arrange
        self.user = UserModel.objects.create_user(username='test',
                                                  email='test@test.com',
                                                  password='12test34')
        self.profile = UserProfile.objects.filter(user=self.user)

    def test__user_creation__creates_profile(self):
        self.assertEqual(1, self.profile.count())
        self.assertEqual(self.user.pk, self.profile.first().pk)

    def test__str_profile__returns_username(self):
        self.assertEqual(self.profile.first().__str__(), 'test')

    def test__full_name__returns_full_name(self):
        profile = self.profile.first()
        profile.first_name = 'Test'
        profile.last_name = 'Testov'
        profile.save()
        self.assertEqual(self.profile.first().full_name(), 'Test Testov')