from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
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
