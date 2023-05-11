from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_login_success(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpass'}
        )
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'wrongpass'}
        )
        self.assertContains(response, 'Please enter a correct username and password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
