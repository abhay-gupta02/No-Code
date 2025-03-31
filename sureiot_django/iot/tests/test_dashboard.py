from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class DashboardViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()  # Get the custom user model
        self.user = self.User.objects.create_user(username='testuser', password='password')

    def test_dashboard_access_with_login(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access_without_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
