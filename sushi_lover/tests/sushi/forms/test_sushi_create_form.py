import os
import tempfile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from sushi_lover.sushi.forms import SushiCreateForm
from sushi_lover.sushi.models import Sushi
from sushi_lover.sushi_type.models import SushiType

UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        user_email = 'sushi_lover@test.net'
        user_password = 'TestPass123'
        self.user = UserModel.objects.create_user(
            email=user_email,
            password=user_password,
        )

        self.user.is_active = True

        self.test_large_image = SimpleUploadedFile(
            name='large_image_test.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'static/images/large_image_test.jpg'), 'rb').read(),
        )

        self.sushi_type = SushiType.objects.create(
            name='TestName',
            description='TestDescription',
            user=self.user,
        )

        self.sushi = Sushi.objects.create(
            label='TestLabelName',
            type=self.sushi_type,
            ingredients='TestIngredient',
            image=tempfile.NamedTemporaryFile(suffix="_test.jpg").name,
            user=self.user,
        )


class TestSushiCreateForm(TestBaseCase):
    def test_sushi_create_form__when_all_fields_filled__expected_form_is_valid(self):
        data = {
            'label': 'TestLabelName',
            'type': self.sushi_type,
            'ingredients': 'TestIngredient',
        }

        files = {'file': tempfile.NamedTemporaryFile(suffix="_test.jpg").name}
        form = SushiCreateForm(data=data, files=files)

        self.assertTrue(form.is_valid())

    def test_sushi_create_form__when_empty_type_field__expected_form_is_not_valid(self):
        data = {
            'label': 'TestLabelName',
            'type': '',
            'ingredients': 'TestIngredient',
        }

        files = {'file': tempfile.NamedTemporaryFile(suffix="_test.jpg").name}
        form = SushiCreateForm(data=data, files=files)

        self.assertEqual(form.errors['type'], ['This field is required.'])
        self.assertEqual(False, form.is_valid())

    def test_sushi_create_form__when_upload_large_image__expected_form_error_and_form_not_valid(self):
        data = {
            'label': 'TestLabelName',
            'type': self.sushi_type,
            'ingredients': 'TestIngredient',
        }

        files = {'image': self.test_large_image, }
        form = SushiCreateForm(data=data, files=files)

        self.assertEqual(form.errors['image'], ['Image size is larger than what is allowed.'])
        self.assertEqual(False, form.is_valid())