"""
video_app.apps
~~~~~~~~~~~~~~

AppConfig for the video_app Django application.

Ensures signals are registered when the app is ready.
"""

from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    """
    Configuration class for the video_app.
    Registers model signals on app ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_app'

    def ready(self):
        from . import signals
