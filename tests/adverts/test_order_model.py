import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from adverts.models import Advertisement, Order
from chat.models import Thread

UserModel = get_user_model()

class OrderModelTestCase(TestCase):
    def setUp(self):
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
        self.order = Order.objects.create(
            advertisement=self.advertisement,
            user=self.user2,
            thread=self.thread,
            created=datetime.datetime(2025, 7, 9, 23, 23, 00)
        )

    def test__order_creation__initiates_default_status_and_amount(self):
        self.assertEqual(self.order.amount, 0)
        self.assertEqual(self.order.status, Order.StatusChoices.CREATED)

    def test__str_order__returns_related_advert_and_creation_date(self):
        self.assertEqual(str(self.order), f'Order for {self.order.advertisement} made on {self.order.created.strftime("%b %d %y")}')