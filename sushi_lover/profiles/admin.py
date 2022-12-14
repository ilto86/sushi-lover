from django.contrib import admin

from sushi_lover.profiles.models import AppProfile


@admin.register(AppProfile)
class AppProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = (
        'username',
        'first_name',
        'last_name',
        'age',
        'image',
        'is_complete',
        'user',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'age',
    )

    list_filter = (
        'username',
        'first_name',
        'last_name',
        'age',
        'image',
        'is_complete',
        'user',
    )

    fieldsets = (
        ('User info', {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'age',
                'image',
                'is_complete',
                'user',
            )}),
    )
