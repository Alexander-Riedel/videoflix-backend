"""
video_app.admin
~~~~~~~~~~~~~~~

Admin configuration for the Video model in the Django admin interface.
"""

from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Video model.
    Displays metadata, enables search and filtering, and marks creation time as read-only.
    """
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'thumbnail', 'video')
        }),
        ('Meta', {
            'fields': ('created_at',),
        }),
    )
