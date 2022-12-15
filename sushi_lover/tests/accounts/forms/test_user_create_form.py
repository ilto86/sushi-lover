from django.test import TestCase

from sushi_lover.accounts.forms import UserCreateForm


class TestUserCreateForm(TestCase):
    def test_user_create_form__when_validation_is_successful(self):
        data = {
            'email': 'sushi_lover@test.net',
            'password1': 'Test_Pass_123',
            'password2': 'Test_Pass_123',
        }

        form = UserCreateForm(data=data)

        self.assertEqual(True, form.is_valid())

    def test_user_create_form__when_empty_form__validation_is_not_successful(self):
        data = {}
        form = UserCreateForm(data=data)

        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])
        self.assertEqual(False, form.is_valid())

    def test_user_create_form__when_email_address_is_not_correct__validation_is_not_successful(self):
        data = {
            'email': 'sushi_lover.net',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
        }

        form = UserCreateForm(data=data)

        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
        self.assertEqual(False, form.is_valid())
