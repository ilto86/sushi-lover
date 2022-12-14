from django import template
from django.contrib.auth import get_user_model

from sushi_lover.core.utilities import get_entity_by_pk
from sushi_lover.profiles.models import AppProfile
from sushi_lover.sushi.models import Sushi
from sushi_lover.sushi_type.models import SushiType
from sushi_lover.sushi_bar.models import SushiBar


register = template.Library()
UserModel = get_user_model()


@register.inclusion_tag('tags/show-profile-complete-notification.html', takes_context=True)
def show_profile_complete_notification(context):
    user_id = context.request.user.id
    profile = get_entity_by_pk(AppProfile, user_id)

    return {
        'profile_id': user_id,
        'is_complete': profile.is_complete,
    }


@register.inclusion_tag('tags/show-profile-username.html', takes_context=True)
def show_profile_username(context):
    user_id = context.request.user.id
    profile = get_entity_by_pk(AppProfile, user_id)

    user = get_entity_by_pk(UserModel, user_id)
    username = user.email.split('@')[0]

    return {
        'profile_id': user_id,
        'profile': profile,
        'username': username,
    }


@register.inclusion_tag('tags/show-profile-progress-bar.html', takes_context=True)
def show_progress_bar(context):
    user_id = context.request.user.id
    profile = get_entity_by_pk(AppProfile, user_id)
    profile_credentials_tuple = (
        profile.username,
        profile.first_name,
        profile.last_name,
        profile.age,
        str(profile.image),
    )
    percentage = 100

    for credential in profile_credentials_tuple:
        if credential is None or credential == '':
            percentage -= 20

    return {
        'percentage': percentage
    }


@register.inclusion_tag('tags/show-profile-stats.html', takes_context=True)
def show_profile_stats(context):
    user = context.request.user

    sushi_all = Sushi.objects.all().filter(user=user)
    sushi_all_count = sushi_all.count()
    sushi_likes_count = 0
    for sushi in sushi_all:
        sushi_likes_count += sushi.sushilike_set.count()

    sushi_types = SushiType.objects.all().filter(user=user)
    sushi_types_count = sushi_types.count()
    sushi_type_likes_count = 0
    for sushi_type in sushi_types:
        sushi_type_likes_count += sushi_type.sushitypelike_set.count()

    sushi_bars = SushiBar.objects.all().filter(user=user)
    sushi_bars_count = sushi_bars.count()
    sushi_bar_likes_count = 0
    for sushi_bar in sushi_bars:
        sushi_bar_likes_count += sushi_bar.sushibarlike_set.count()

    return {
        'sushi_types_count': sushi_types_count,
        'sushi_all_count': sushi_all_count,
        'sushi_bars_count': sushi_bars_count,
        'sushi_type_likes_count': sushi_type_likes_count,
        'sushi_likes_count': sushi_likes_count,
        'sushi_bar_likes_count': sushi_bar_likes_count,
    }
