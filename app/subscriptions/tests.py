from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Subscription

User = get_user_model()

class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(email = 'test1@gmail.com', password = 'pw123')
        self.user2 = User.objects.create_user(email = 'test2@gmail.com', password = 'pw123')

        self.client.force_authenticate(user = self.user1)

    def test_create_subscription(self):
        response = self.client.post('/api/v1/subscriptions/', {'subscribed_to':self.user2.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(subscriber = self.user1, subscribed_to = self.user2).exists())

    def test_create_subscription_to_self(self):
        response = self.client.post('/api/v1/subscriptions/', {'subscribed_to': self.user1.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_subscription(self):
        Subscription.objects.create(subscriber = self.user1, subscribed_to = self.user2)
        response = self.client.post('/api/v1/subscriptions/', {'subscribed_to': self.user2.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(subscriber = self.user1, subscribed_to = self.user2)
        response = self.client.delete(f'/api/v1/subscriptions/{self.user2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(id = subscription.id).exists())

    def test_delete_nonexistent_subscription(self):
        response = self.client.delete(f'/api/v1/subscriptions/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)