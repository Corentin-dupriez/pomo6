from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from adverts.models import Advertisement, Order
from chat.models import Thread

UserModel = get_user_model()

class TestAdvertisementAPIViews(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        self.staff_user = UserModel.objects.create_user(
            username="staffuser",
            email="<EMAIL>",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.advert = Advertisement.objects.create(
            title="Test Advertisement",
            slug="test-advertisement",
            description="Test description",
            category=Advertisement.CategoryChoices.IT_HELP,
            fixed_price=50,
            user=self.user,
        )

    def test__predict_category_with_title__returns_prediction(self):
        self.client.login(username='testuser', password="<PASSWORD>")
        response = self.client.post(reverse('predict_category'), data={'title': 'I will test your django website.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.json()['predicted_category'], Advertisement.CategoryChoices)

    def test__predict_category_without_title__returns_400(self):
        self.client.login(username='testuser', password="<PASSWORD>")
        response = self.client.post(reverse('predict_category'), data={'title': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'title is required')

    def test__approve_existing_listing_by_staff__approves_listing(self):
        self.client.login(username='staffuser', password="<PASSWORD>")
        self.assertFalse(self.advert.approved)
        response = self.client.patch(reverse('approve_listing',
                                             kwargs={'pk': self.advert.pk}),
                                             data={'approved': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')
        self.advert.refresh_from_db()
        self.assertTrue(self.advert.approved)

    def test__approve_existing_listing_by_regular_user__raises_403(self):
        self.client.login(username='testuser', password="<PASSWORD>")
        response = self.client.patch(reverse('approve_listing', kwargs={'pk': self.advert.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__change_order_status__updates_order_status(self):
        user2 = UserModel.objects.create_user(
            username="user2",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        thread = Thread.objects.create(advert=self.advert)
        thread.participants.add(self.user,
                                     user2,)
        order = Order.objects.create(
            advertisement=self.advert,
            user=user2,
            thread=thread,
        )
        self.client.login(username='testuser', password="<PASSWORD>")
        response = self.client.patch(reverse('update_order_status',
                                             kwargs={'pk': order.pk}),
                                     data={'status': Order.StatusChoices.APPROVED})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')
        order.refresh_from_db()
        self.assertEqual(order.status, Order.StatusChoices.APPROVED)

    def test__change_order_status_by_other_user__raises_403(self):
        user2 = UserModel.objects.create_user(
            username="user2",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        thread = Thread.objects.create(advert=self.advert)
        thread.participants.add(self.user,
                                user2, )
        order = Order.objects.create(
            advertisement=self.advert,
            user=user2,
            thread=thread,
        )
        self.client.login(username='staffuser', password="<PASSWORD>")
        response = self.client.patch(reverse('update_order_status',
                                             kwargs={'pk': order.pk}),
                                     data={'status': Order.StatusChoices.APPROVED})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.StatusChoices.CREATED)