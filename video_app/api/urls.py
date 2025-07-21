from django.urls import path
from .views import VideoListAPIView, HLSPlaylistAPIView, HLSSegmentAPIView

urlpatterns = [
    path('video/', VideoListAPIView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8',
         HLSPlaylistAPIView.as_view(), name='video-playlist'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/',
         HLSSegmentAPIView.as_view(), name='video-segment'),
]