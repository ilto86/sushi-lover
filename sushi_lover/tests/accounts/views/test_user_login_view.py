from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        user_email = 'sushi_lover@test.net'
        user_password = 'TestPass123'
        self.user = UserModel.objects.create_user(
            email=user_email,
            password=user_password,
        )


class TestUserLoginView(TestBaseCase):
    def test_user_login_view(self):
        response = self.client.get(reverse_lazy('sign in'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please fill all the fields to Login')

    def test_user_login_view__when_sign_in_is_successful__and_redirected_to_homepage(self):
        self.client.login(username='sushi_lover@test.net', password='TestPass123')

        user = auth.get_user(self.client)
        data = {'user': user}

        response = self.client.post(reverse_lazy('sign in'), data)

        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_user_login_view__when_sign_in__is_not_successful(self):
        self.client.login(email='test@sushi.com', password='123TestPass')

        user = auth.get_user(self.client)
        data = {'user': user}

        response = self.client.post(reverse_lazy('sign in'), data)

        self.assertEqual(False, user.is_authenticated)
        self.assertEqual(response.status_code, 200)