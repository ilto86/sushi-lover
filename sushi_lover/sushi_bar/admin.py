from django.contrib import admin

from sushi_lover.sushi_bar.models import SushiBar, SushiBarLike, SushiBarComment


@admin.register(SushiBar)
class SushiBarAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'description',
        'image',
        'longitude',
        'latitude',
        'user',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
        'user',
    )
    fieldsets = (
        ('Sushi bar info', {
            'fields': (
                'name',
                'address',
                'description',
                'image',
                'longitude',
                'latitude',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi bar', {
            'classes': (
                'wide',
            ),
            'fields': (
                'name',
                'address',
                'description',
                'image',
                'longitude',
                'latitude',
                'user',
            ),
        }),
    )


@admin.register(SushiBarLike)
class SushiBarLikeAdmin(admin.ModelAdmin):
    list_display = (
        'sushi_bar',
        'user',
    )
    search_fields = (
        'sushi_bar',
    )
    list_filter = (
        'sushi_bar',
        'user',
    )
    fieldsets = (
        ('Sushi bar like', {
            'fields': (
                'sushi_bar',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi bar like', {
            'classes': (
                'wide',
            ),
            'fields': (
                'sushi_bar',
                'user',
            ),
        }),
    )


@admin.register(SushiBarComment)
class SushiBarCommentAdmin(admin.ModelAdmin):
    list_display = (
        'comment',
        'sushi_bar',
        'user',
    )
    search_fields = (
        'sushi_bar',
    )
    list_filter = (
        'sushi_bar',
        'user',
    )
    fieldsets = (
        ('Sushi bar comments', {
            'fields': (
                'comment',
                'sushi_bar',
                'user',
            )}),
    )
    add_fieldsets = (
        ('Sushi bar comments', {
            'classes': (
                'wide',
            ),
            'fields': (
                'comment',
                'sushi_bar',
                'user',
            ),
        }),
    )