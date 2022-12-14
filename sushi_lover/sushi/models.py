from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model

from sushi_lover.sushi_type.models import SushiType

UserModel = get_user_model()


class Sushi(models.Model):
    MAX_LABEL_LENGTH = 20
    MAX_INGREDIENTS_LENGTH = 150

    label = models.CharField(
        max_length=MAX_LABEL_LENGTH,
        blank=False,
        null=False,
    )

    type = models.ForeignKey(
        SushiType,
        on_delete=models.CASCADE,
    )

    ingredients = models.TextField(
        max_length=MAX_INGREDIENTS_LENGTH,
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to='sushi',
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class SushiLike(models.Model):
    sushi = models.ForeignKey(
        Sushi,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class SushiComment(models.Model):
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

    sushi = models.ForeignKey(
        Sushi,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
