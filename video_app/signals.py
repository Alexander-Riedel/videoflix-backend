from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save
print("⚙️ signals.py geladen")


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New video created')