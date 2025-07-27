"""
video_app.signals
~~~~~~~~~~~~~~~~~

This module defines Django signal receivers for the Video model.

- On video creation: enqueue HLS conversion task (via django_rq)
- On video deletion: remove the associated video file from the file system
"""

import os
import django_rq
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Video
from video_app.tasks import convert_to_hls


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal triggered after a Video instance is saved.

    If the instance is newly created, it enqueues a background task
    to convert the uploaded video into HLS format using django_rq.
    """
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_to_hls, instance.video.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Signal triggered after a Video instance is deleted.

    If the video file exists on the file system, it will be removed to
    prevent orphaned files from taking up space.
    """
    if instance.video and os.path.isfile(instance.video.path):
        os.remove(instance.video.path)
