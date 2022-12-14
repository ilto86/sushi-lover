from django.contrib import admin

from sushi_lover.sushi_type.models import SushiType, SushiTypeLike, SushiTypeComment


@admin.register(SushiType)
class SushiTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'image',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
        'description',
        'image',
    )
    fieldsets = (
        ('Sushi type', {
            'fields': (
                'name',
                'description',
                'image',
            )}),
    )
    add_fieldsets = (
        ('Sushi type', {
            'classes': (
                'wide',
            ),
            'fields': (
                'name',
                'description',
                'image',
            ),
        }),
    )


@admin.register(SushiTypeLike)
class SushiTypeLikeAdmin(admin.ModelAdmin):
    list_display = (
        'sushi_type',
        'user',
    )
    search_fields = (
        'sushi_type',
    )
    list_filter = (
        'sushi_type',
        'user',
    )
    fieldsets = (
        ('Sushi type like', {
            'fields': (
                'sushi_type',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi type like', {
            'classes': (
                'wide',
            ),
            'fields': (
                'sushi_type',
                'user',
            ),
        }),
    )


@admin.register(SushiTypeComment)
class SushiTypeCommentAdmin(admin.ModelAdmin):
    list_display = (
        'comment',
        'sushi_type',
        'user',
    )
    search_fields = (
        'sushi_type',
    )
    list_filter = (
        'sushi_type',
        'user',
    )
    fieldsets = (
        ('Sushi type comments', {
            'fields': (
                'comment',
                'sushi_type',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi type comments', {
            'classes': (
                'wide',
            ),
            'fields': (
                'comment',
                'sushi_type',
                'user',
            ),
        }),
    )