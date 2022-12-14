from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from sushi_lover.accounts.forms import UserCreateForm

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(BaseUserAdmin):
    add_form = UserCreateForm

    list_display = ('email', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('date_joined',)
    filter_horizontal = ()