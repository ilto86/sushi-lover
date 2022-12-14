from django import forms
from django.contrib.auth import forms as auth_forms, hashers as auth_hashers, get_user_model, authenticate

UserModel = get_user_model()


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Enter your password',
                'name': 'width: 1px',
                'class': 'form-control',
            }
        )
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Confirm your password',
                'name': 'width: 1px',
                'class': 'form-control',
            }
        ),
    )

    class Meta:
        model = UserModel
        fields = ('email',)
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter valid email address',
                'name': 'width: 1px',
                'class': 'form-control',
            }
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                try:
                    user = UserModel.objects.get(email=username)
                    if not auth_hashers.check_password(password, user.password):
                        raise forms.ValidationError(
                            {'password': 'Incorrect password.'}
                        )
                    elif not user.is_active:
                        raise forms.ValidationError(
                            {'username': 'Inactive account.'}
                        )
                except UserModel.DoesNotExist:
                    raise forms.ValidationError(
                        {'username': 'Incorrect email.'}
                    )

        return super().clean()

    def save(self):
        return UserModel

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'placeholder': 'Enter valid email address',
                'name': 'width: 1px',
                'class': 'form-control',
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': 'Enter your password',
                'name': 'width: 1px',
                'class': 'form-control',
            }
        ),
    )
