from django import forms

from sushi_lover.core import utilities as my_utilities
from sushi_lover.core import validators as my_validators
from sushi_lover.sushi.models import Sushi, SushiComment


class SushiCreateForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            my_validators.ImageSizeValidator.image_size_validator(image)

        return image

    class Meta:
        model = Sushi
        exclude = ('user',)
        widgets = {
            'label': forms.TextInput(
                attrs={
                    'placeholder': 'Enter sushi name here',
                    'style': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'type': forms.Select(
                attrs={
                    'style': 'width: 400px',
                    'class': 'form-select'
                }
            ),

            'ingredients': forms.Textarea(
                attrs={
                    'placeholder': 'Write here the sushi ingredients',
                    'rows': 6,
                    'cols': 60,
                    'style': 'resize: none',
                    'class': 'form-control',
                }
            ),

            'image': forms.FileInput(
                attrs={
                    'style': 'width: 145; height: 200',
                    'class': 'form-control',
                }
            ),
        }


class SushiEditForm(SushiCreateForm):
    def save(self, commit=True):
        my_utilities.delete_previous_image(self, commit, Sushi, 'empty-plate-without-sushi.jpg')
        return super().save(commit=commit)


class SushiCommentForm(forms.ModelForm):
    object_pk = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) < SushiComment.MIN_COMMENT_LENGTH:
            raise forms.ValidationError(f'Comment must be at least {SushiComment.MIN_COMMENT_LENGTH} characters long.')
        return comment

    def save(self, commit=True):
        sushi_pk = self.cleaned_data['object_pk']
        sushi = Sushi.objects.get(pk=sushi_pk)
        comment = SushiComment(
            comment=self.cleaned_data['comment'],
            sushi=sushi,
        )

        if commit:
            comment.save()

        return comment

    class Meta:
        model = SushiComment
        fields = ('comment', 'object_pk')
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Enter yor comment for this sushi here.',
                    'rows': 6,
                    'cols': 60,
                    'style': 'resize: none; background-color:transparent',
                    'class': 'form-control',
                }
            )
        }
