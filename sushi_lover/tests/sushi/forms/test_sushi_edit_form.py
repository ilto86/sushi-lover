import tempfile
from django.contrib.auth import get_user_model
from django.test import TestCase


from sushi_lover.sushi.forms import SushiCreateForm, SushiEditForm
from sushi_lover.sushi_type.models import SushiType

UserModel = get_user_model()


class TestBaseCase(TestCase):
    def setUp(self):
        user_email = 'sushi_lover@test.com'
        user_password = 'TestPass123'
        self.user = UserModel.objects.create_user(
            email=user_email,
            password=user_password,
        )

        self.sushi_type = SushiType.objects.create(
            name='TestName',
            description='TestDescription',
            user=self.user,
        )


class TestSushiEditForm(TestBaseCase):
    def test_sushi_edit_form__when_all_fields_filled_as_the_fields_of_create_form__expected_form_is_valid(self):
        test_first_image = tempfile.NamedTemporaryFile(suffix="_test.jpg").name,
        test_first_data = {
            'label': 'TestLabelName_1',
            'type': self.sushi_type,
            'ingredients': 'TestIngredient_1',
        }

        first_file_test = {'file': test_first_image}

        create_form = SushiCreateForm(data=test_first_data, files=first_file_test)

        test_second_image = tempfile.NamedTemporaryFile(suffix="_test.jpg").name,
        test_second_data = {
            'label': 'TestLabelName_2',
            'type': self.sushi_type,
            'ingredients': 'TestIngredient_2',
        }

        second_file_test = {'file': test_second_image}

        edit_form = SushiEditForm(data=test_second_data, files=second_file_test)

        self.assertTrue(create_form.is_valid)
        self.assertTrue(edit_form.is_valid)

        self.assertEqual(create_form.data['label'], 'TestLabelName_1')
        self.assertEqual(edit_form.data['label'], 'TestLabelName_2')
        self.assertNotEqual(create_form.data['label'], edit_form.data['label'])

        self.assertEqual(create_form.data['type'], self.sushi_type)
        self.assertEqual(edit_form.data['type'], self.sushi_type)
        self.assertEqual(create_form.data['type'], edit_form.data['type'])

        self.assertEqual(create_form.data['ingredients'], 'TestIngredient_1')
        self.assertEqual(edit_form.data['ingredients'], 'TestIngredient_2')
        self.assertNotEqual(create_form.data['ingredients'], edit_form.data['ingredients'])

        self.assertEqual(create_form.files['file'], test_first_image)
        self.assertEqual(edit_form.files['file'], test_second_image)
        self.assertNotEqual(create_form.files['file'], edit_form.files['file'])