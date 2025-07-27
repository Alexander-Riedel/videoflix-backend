from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    video = models.FileField(upload_to="videos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def hls_directory(self):
        return self.video.path.replace(".mp4", "") + "_hls/"

    def __str__(self):
        return self.title