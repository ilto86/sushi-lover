from django import forms

from sushi_lover.profiles.models import AppProfile
from sushi_lover.core.utilities import delete_previous_image
from sushi_lover.core.validators import ImageSizeValidator


class AppProfileForm(forms.ModelForm):
    def save(self, commit=True):
        delete_previous_image(self, commit, AppProfile, 'anonymous_profile_img.jpg')
        return super().save(commit=commit)

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            ImageSizeValidator.image_size_validator(image)

        return image

    class Meta:
        model = AppProfile
        exclude = ('is_complete', 'user',)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your username',
                    'name': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your first name',
                    'name': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your last name',
                    'name': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'age': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter your age',
                    'name': 'width: 400px',
                    'class': 'form-control',
                }
            ),

            'image': forms.FileInput(
                attrs={
                    'name': 'width: 145; height: 200',
                    'class': 'form-control',
                }
            ),
        }