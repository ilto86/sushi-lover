from django.contrib.auth import get_user_model
from django.test import TestCase

from sushi_lover.accounts.forms import UserLoginForm

UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        first_user_email = 'sushi_lover@test.net'
        first_user_password = 'TestPass123'
        self.first_user = UserModel.objects.create_user(
            email=first_user_email,
            password=first_user_password,
        )

        second_user_email = 'sushi_hater@test.net'
        second_user_password = 'TestPass456'
        self.second_user = UserModel.objects.create_user(
            email=second_user_email,
            password=second_user_password,
        )


class TestUserLoginForm(TestBaseCase):
    def test_user_login_form__when_login_is_successful(self):
        data = {
            'username': 'sushi_lover@test.net',
            'password': 'TestPass123',
        }

        form = UserLoginForm(data=data)

        self.assertEqual(True, form.is_valid())

    def test_user_login_form__when_empty_form__login_is_not_successful(self):
        data = {}
        form = UserLoginForm(data=data)

        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['password'], ['This field is required.'])
        self.assertEqual(False, form.is_valid())

    def test_user_login_form__when_empty_username_field__login_is_not_successful(self):
        data = {
            'password': 'Test_Pass_123'
        }

        form = UserLoginForm(data=data)

        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(False, form.is_valid())

    def test_user_login_form__when_empty_password_field__login_is_not_successful(self):
        data = {
            'username': 'sushi_lover@test.net',
        }

        form = UserLoginForm(data=data)

        self.assertEqual(form.errors['password'], ['This field is required.'])
        self.assertEqual(False, form.is_valid())

    def test_user_login_form__when_email_address_is_not_correct__login_is_not_successful(self):
        data = {
            'username': 'sushi_lover@sushi.net',
            'password': 'Test_Pass_123',
        }

        form = UserLoginForm(data=data)

        self.assertEqual(form.errors['username'], ['Incorrect email.'])
        self.assertEqual(False, form.is_valid())

    def test_user_login_form__when_password_is_not_correct__login_is_not_successful(self):
        data = {
            'username': 'sushi_hater@test.net',
            'password': 'TestPass123',
        }

        form = UserLoginForm(data=data)

        self.assertEqual(form.errors['password'], ['Incorrect password.'])
        self.assertEqual(False, form.is_valid())

    def test_user_login_form__when_user_is_not_active__login_is_not_successful(self):
        self.second_user.is_active = False
        self.second_user.save()

        data = {
            'username': 'sushi_hater@test.net',
            'password': 'TestPass456',
        }

        form = UserLoginForm(data=data)

        self.assertEqual(form.errors['username'], ['Inactive account.'])
        self.assertEqual(False, form.is_valid())