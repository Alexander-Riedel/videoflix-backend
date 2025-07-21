from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    video = models.FileField(upload_to='videos/', blank=True)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    # Ordnerstruktur: media/videos/{id}/{resolution}/index.m3u8
    def get_playlist_path(self, resolution: str) -> str:
        return f'{self.id}/{resolution}/index.m3u8'

    def get_segment_path(self, resolution: str, segment: str) -> str:
        return f'{self.id}/{resolution}/{segment}'

    def __str__(self):
        return self.title