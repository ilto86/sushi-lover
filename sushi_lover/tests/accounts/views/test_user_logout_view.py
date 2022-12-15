from django.contrib.auth import get_user_model
from django.db.models import signals
from django.test import TestCase, Client
from django.urls import reverse

UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        self.client = Client()
        signals.post_save.receivers = []

        user_email = 'sushi_lover@test.net'
        user_password = 'TestPass123'
        self.user = UserModel.objects.create_user(
            email=user_email,
            password=user_password,
        )


class TestUserLogoutView(TestBaseCase):
    def test_user_logout_view__when_sign_out_is_successful(self):
        self.client.force_login(self.user)
        self.client.logout()
        response = self.client.post(reverse('sign out'))
        self.assertEqual(response.status_code, 302)