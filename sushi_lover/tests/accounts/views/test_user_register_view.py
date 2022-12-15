from django.contrib.auth import get_user_model
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse_lazy

UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        signals.post_save.receivers = []

        user_email = 'sushi_lover@test.net'
        user_password = 'TestPass123'
        self.user = UserModel.objects.create_user(
            email=user_email,
            password=user_password,
        )


class TestSignUpView(TestBaseCase):
    def test_user_sign_up_view(self):
        response = self.client.get(reverse_lazy('sign up'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please fill all the fields to Create Account')

