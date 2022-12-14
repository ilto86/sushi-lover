from django import forms

from sushi_lover.core import utilities as my_utilities
from sushi_lover.core import validators as my_validators
from sushi_lover.sushi_bar.models import SushiBar, SushiBarComment


class SushiBarCreateForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            my_validators.ImageSizeValidator.image_size_validator(image)

        return image

    class Meta:
        model = SushiBar
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter sushi bar name here',
                    'style': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Enter sushi bar address here',
                    'style': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Write something about this sushi bar',
                    'rows': 5,
                    'cols': 50,
                    'style': 'resize: none',
                    'class': 'form-control',
                }
            ),

            'website': forms.URLInput(
                attrs={
                    'placeholder': 'Enter valid url',
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


class SushiBarEditForm(SushiBarCreateForm):
    def save(self, commit=True):
        my_utilities.delete_previous_image(self, commit, SushiBar, 'no_sushi_bar.jpg')
        return super().save(commit=commit)


class SushiBarCommentForm(forms.ModelForm):
    object_pk = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    def save(self, commit=True):
        sushi_bar_pk = self.cleaned_data['object_pk']
        sushi_bar = SushiBar.objects.get(pk=sushi_bar_pk)
        comment = SushiBarComment(
            comment=self.cleaned_data['comment'],
            sushi_bar=sushi_bar,
        )

        if commit:
            comment.save()

        return comment

    class Meta:
        model = SushiBarComment
        fields = ('comment', 'object_pk')
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Enter yor comment for this sushi bar here.',
                    'rows': 6,
                    'cols': 60,
                    'style': 'resize: none; background-color:transparent',
                    'class': 'form-control',
                }
            )
        }