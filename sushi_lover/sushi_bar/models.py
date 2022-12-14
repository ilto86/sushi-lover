from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class SushiBar(models.Model):
    MAX_NAME_LENGTH = 20
    MAX_ADDRESS_LENGTH = 60
    MAX_DESCRIPTION_LENGTH = 150
    MAX_DIGITS_LENGTH = 9
    MAX_DECIMAL_PLACES_LENGTH = 6

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=False,
        null=False,
    )

    address = models.TextField(
        max_length=MAX_ADDRESS_LENGTH,
        blank=True,
        null=True,
    )

    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to='sushi_bars',
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=MAX_DIGITS_LENGTH,
        decimal_places=MAX_DECIMAL_PLACES_LENGTH,
        blank=True,
        null=True,
    )

    latitude = models.DecimalField(
        max_digits=MAX_DIGITS_LENGTH,
        decimal_places=MAX_DECIMAL_PLACES_LENGTH,
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class SushiBarLike(models.Model):
    sushi_bar = models.ForeignKey(
        SushiBar,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class SushiBarComment(models.Model):
    MAX_COMMENT_LENGTH = 180
    MIN_COMMENT_LENGTH = 5

    comment = models.TextField(
        max_length=MAX_COMMENT_LENGTH,
        validators=(
            validators.MinLengthValidator(MIN_COMMENT_LENGTH),
        ),
        blank=True,
        null=True,
    )

    sushi_bar = models.ForeignKey(
        SushiBar,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

