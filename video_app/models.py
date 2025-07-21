from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title