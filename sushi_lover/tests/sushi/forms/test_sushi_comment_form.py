from django.test import TestCase


from sushi_lover.sushi.forms import SushiCommentForm


class TestSushiCommentForm(TestCase):
    def test_sushi_comment_form__when_comment_is_created__expected_form_is_valid(self):
        data = {
            'comment': 'This is a valid comment',
            'object_pk': 1,
        }

        form = SushiCommentForm(data=data)

        self.assertTrue(form.is_valid())

    def test_sushi_comment_form__when_comment_is_too_short__expected_form_is_not_valid_and_error_message(self):
        data = {
            'comment': '1234',
            'object_pk': 1,
        }

        form = SushiCommentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['Comment must be at least 5 characters long.'])

    def test_sushi_comment_form__when_missing_object_pk_field_comment_is_not_valid__expected_form_is_not_valid(self):
        data = {'comment': 'This is a valid comment'}
        form = SushiCommentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['object_pk'], ['This field is required.'])
