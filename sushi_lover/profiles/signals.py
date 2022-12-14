import os
from sushi_lover.core.utilities import get_entity_by_pk
from django.conf import settings
from django.db.models.signals import pre_delete, post_save, pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from sushi_lover.profiles.models import AppProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = AppProfile(
            user=instance,
        )
        profile.save()
        print("profile_signal")


@receiver(pre_save, sender=AppProfile)
def is_profile_complete(sender, instance, **kwargs):
    if instance.username and instance.first_name \
            and instance.last_name and instance.age \
            and instance.image:

        instance.is_complete = True
    else:
        instance.is_complete = False


@receiver(pre_delete, sender=UserModel)
def delete_image_when_delete_account(sender, instance, **kwargs):
    current_profile = get_entity_by_pk(AppProfile, instance.pk)
    current_profile_image_location = os.path.join(settings.MEDIA_ROOT, str(instance.email))

    if current_profile.image:
        current_profile.image.delete()

    if os.path.isdir(current_profile_image_location):
        os.rmdir(current_profile_image_location)