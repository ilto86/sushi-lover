from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class SushiType(models.Model):
    MAX_NAME_LENGTH = 20
    MAX_DESCRIPTION_LENGTH = 150

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=False,
        null=False,
    )

    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to='sushi_type',
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class SushiTypeLike(models.Model):
    sushi_type = models.ForeignKey(
        SushiType,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class SushiTypeComment(models.Model):
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

    sushi_type = models.ForeignKey(
        SushiType,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )