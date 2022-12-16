from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse_lazy


UserModel = get_user_model()


class TestUserRegisterView(TestCase):
    def test_user_register_view(self):
        response = self.client.get(reverse_lazy('sign up'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please fill all the fields to Create Account')

    def test_user_register_view__when_sign_up_and_login_is_successful(self):
        user_email = 'sushi_lover@test.net'
        user_password = 'TestPass123'

        data = {
            'email': user_email,
            'password1': user_password,
            'password2': user_password,
        }

        response = self.client.post(reverse_lazy('sign up'), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserModel.objects.filter(email=data['email']).exists())
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_user_register_view__when_send_greeting_email_is_successful(self):
        user_email = 'sushi_lover@test.net'
        user_password = 'TestPass123'

        data = {
            'email': user_email,
            'password1': user_password,
            'password2': user_password,
        }

        self.client.post(reverse_lazy('sign up'), data=data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [data['email']])
        self.assertEqual(mail.outbox[0].subject, 'Welcome to our Sushi Lover Page!')

