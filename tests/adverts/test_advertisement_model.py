from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify

from adverts.models import Advertisement, Views

UserModel = get_user_model()

class TestAdvertisementModel(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='test', email='test@test.com', password='12test34')
        self.advertisement = Advertisement.objects.create(
            title='Test Advertisement',
            description='Test description',
            user=self.user,
            category=Advertisement.CategoryChoices.IT_HELP,
            fixed_price=100,
        )

    def test__advertisement_slug__created_automatically_is_slugified_title(self):
        self.assertEqual(self.advertisement.slug, slugify(self.advertisement.title))

    def test__increase_view__creates_a_view_for_advertisement(self):
        self.assertEqual(Views.objects.filter(advertisement=self.advertisement).count(), 0)
        self.advertisement.increase_views()
        self.assertEqual(Views.objects.filter(advertisement=self.advertisement).count(), 1)

    def test__approving_advert__advert_is_approved(self):
        self.assertFalse(self.advertisement.approved)
        self.advertisement.approve_listings()
        self.assertTrue(self.advertisement.approved)

    def test__str_of_advertisement__returns_title(self):
        self.assertEqual(str(self.advertisement), self.advertisement.title)
