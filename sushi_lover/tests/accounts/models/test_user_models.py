from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import signals
from django.test import TestCase


UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        signals.post_save.receivers = []

        user_email = 'first_test@abv.com'
        user_password = 'TestPass123'
        self.user = UserModel.objects.create_user(
            email=user_email,
            password=user_password,
        )


class TestAppUserModel(TestBaseCase):
    def test_user_model__when_model_types_are_correct__expect_result_is_successful(self):
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.date_joined, datetime)
        self.assertIsInstance(self.user.last_login, datetime)
        self.assertIsInstance(self.user.is_active, bool)
        self.assertIsInstance(self.user.is_staff, bool)
        self.assertIsInstance(self.user.is_superuser, bool)

    def test_user_model__when_model_type_validations_is_correct__expect_result_is_successful(self):
        self.assertEqual(True, self.user._meta.get_field('email').unique)
        self.assertEqual(True, self.user._meta.get_field('date_joined').auto_now_add)
        self.assertEqual(True, self.user._meta.get_field('last_login').auto_now)
        self.assertTrue(self.user._meta.get_field('is_active').default)
        self.assertFalse(self.user._meta.get_field('is_staff').default)
        self.assertEqual(False, self.user._meta.get_field('is_superuser').default)