from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from sushi_lover.accounts.models import AppUser
from sushi_lover.core.utilities import image_upload_location

UserModel = get_user_model()


class AppProfile(models.Model):
    MIN_USERNAME_LENGTH = 2
    MAX_USERNAME_LENGTH = 15

    MIN_FIRST_NAME_LENGTH = 2
    MAX_FIRST_NAME_LENGTH = 15

    MIN_LAST_NAME_LENGTH = 2
    MAX_LAST_NAME_LENGTH = 15

    AGE_MIN_VALUE = 16

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_USERNAME_LENGTH),
        ),
        blank=True,
        null=True,
    )

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_FIRST_NAME_LENGTH),
        ),
        blank=True,
        null=True,
        verbose_name='First Name',
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_LAST_NAME_LENGTH),
        ),
        blank=True,
        null=True,
        verbose_name='Last Name',
    )

    age = models.PositiveIntegerField(
        validators=(
            MinValueValidator(AGE_MIN_VALUE,
            _(f"You must be {AGE_MIN_VALUE} years old or above.")),
        ),
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to=image_upload_location,
        blank=True,
        null=True,
    )

    is_complete = models.BooleanField(
        default=False,
    )

    user = models.OneToOneField(
        UserModel,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    class Meta:
        ordering = ('pk',)
