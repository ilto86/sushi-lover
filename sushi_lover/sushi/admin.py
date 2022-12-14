from django.contrib import admin

from sushi_lover.sushi.models import Sushi, SushiLike, SushiComment


@admin.register(Sushi)
class SushiAdmin(admin.ModelAdmin):
    list_display = (
        'label',
        'type',
        'ingredients',
        'image',
        'user',
    )
    search_fields = (
        'label',
        'type',
    )
    list_filter = (
        'label',
        'type',
        'ingredients',
        'image',
        'user',
    )
    fieldsets = (
        ('Sushi info', {
            'fields': (
                'label',
                'type',
                'ingredients',
                'image',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi', {
            'classes': (
                'wide',
            ),
            'fields': (
                'label',
                'type',
                'ingredients',
                'image',
                'user',
            ),
        }),
    )


@admin.register(SushiLike)
class SushiLikeAdmin(admin.ModelAdmin):
    list_display = (
        'sushi',
        'user',
    )
    search_fields = (
        'sushi',
    )
    list_filter = (
        'sushi',
        'user',
    )
    fieldsets = (
        ('Sushi like', {
            'fields': (
                'sushi',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi like', {
            'classes': (
                'wide',
            ),
            'fields': (
                'sushi',
                'user',
            ),
        }),
    )


@admin.register(SushiComment)
class SushiCommentAdmin(admin.ModelAdmin):
    list_display = (
        'comment',
        'sushi',
        'user',
    )
    search_fields = (
        'sushi',
    )
    list_filter = (
        'sushi',
        'user',
    )
    fieldsets = (
        ('Sushi comments', {
            'fields': (
                'comment',
                'sushi',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi comments', {
            'classes': (
                'wide',
            ),
            'fields': (
                'comment',
                'sushi',
                'user',
            ),
        }),
    )
