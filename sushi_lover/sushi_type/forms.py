from django import forms

from sushi_lover.core import utilities as my_utilities
from sushi_lover.core import validators as my_validators
from sushi_lover.sushi_type.models import SushiType, SushiTypeComment


class SushiTypeCreateForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            my_validators.ImageSizeValidator.image_size_validator(image)

        return image

    class Meta:
        model = SushiType
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter sushi type name here',
                    'style': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Write something about this sushi type',
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


class SushiTypeEditForm(SushiTypeCreateForm):
    def save(self, commit=True):
        my_utilities.delete_previous_image(self, commit, SushiType, 'empty-plate-without-sushi.jpg')
        return super().save(commit=commit)


class SushiTypeCommentForm(forms.ModelForm):
    object_pk = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    def save(self, commit=True):
        sushi_type_pk = self.cleaned_data['object_pk']
        sushi_type = SushiType.objects.get(pk=sushi_type_pk)
        comment = SushiTypeComment(
            comment=self.cleaned_data['comment'],
            sushi_type=sushi_type,
        )

        if commit:
            comment.save()

        return comment

    class Meta:
        model = SushiTypeComment
        fields = ('comment', 'object_pk')
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Enter yor comment for this sushi type here.',
                    'rows': 6,
                    'cols': 60,
                    'style': 'resize: none; background-color:transparent',
                    'class': 'form-control',
                }
            )
        }