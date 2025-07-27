"""
video_app.models
~~~~~~~~~~~~~~~~

This module defines the Video model used for storing video metadata
and files in the Videoflix application.
"""

from django.db import models


class Video(models.Model):
    """
    Represents a video uploaded to the platform, including metadata,
    thumbnail, original video file, and creation timestamp.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    video = models.FileField(upload_to="videos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def hls_directory(self):
        """
        Returns the file system path to the folder where HLS segments are stored.

        Returns:
            str: Path to the corresponding HLS folder for the video.
        """
        return self.video.path.replace(".mp4", "") + "_hls/"

    def __str__(self):
        """
        Returns the string representation of the video object.

        Returns:
            str: The video title.
        """
        return self.title
