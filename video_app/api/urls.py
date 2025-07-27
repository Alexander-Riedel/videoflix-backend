"""
video_app.api.urls
~~~~~~~~~~~~~~~~~~

Defines API routes for listing videos and streaming HLS content (playlists and segments).
"""

from django.urls import path
from .views import VideoListView, stream_m3u8, stream_segment

urlpatterns = [
    path('video/', VideoListView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', stream_m3u8, name='stream-m3u8'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', stream_segment, name='stream-segment'),
]
