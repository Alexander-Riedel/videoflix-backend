import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from video_app.models import Video
from .serializers import VideoSerializer


class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

class HLSPlaylistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, movie_id, resolution):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")
        path = video.get_playlist_path(resolution)
        full_path = os.path.join(settings.MEDIA_ROOT, 'videos', path)
        if not os.path.exists(full_path):
            raise Http404("Manifest not found")
        return FileResponse(open(full_path, 'rb'), content_type='application/vnd.apple.mpegurl')

class HLSSegmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")
        path = video.get_segment_path(resolution, segment)
        full_path = os.path.join(settings.MEDIA_ROOT, 'videos', path)
        if not os.path.exists(full_path):
            raise Http404("Segment not found")
        return FileResponse(open(full_path, 'rb'), content_type='video/MP2T')
