# video_app/api/views.py

import os
from django.http import FileResponse, Http404
from video_app.models import Video

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class VideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all()
        data = [{
            "id": v.id,
            "created_at": v.created_at,
            "title": v.title,
            "description": v.description,
            "thumbnail_url": request.build_absolute_uri(v.thumbnail.url),
            "category": v.category
        } for v in videos]
        return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_m3u8(request, movie_id, resolution):
    try:
        video = Video.objects.get(pk=movie_id)
        base = os.path.splitext(video.video.path)[0]
        hls_path = f"{base}_hls/{resolution}/index.m3u8"
        return FileResponse(open(hls_path, 'rb'), content_type="application/vnd.apple.mpegurl")
    except (Video.DoesNotExist, FileNotFoundError):
        raise Http404()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_segment(request, movie_id, resolution, segment):
    try:
        video = Video.objects.get(pk=movie_id)
        base = os.path.splitext(video.video.path)[0]
        segment_path = f"{base}_hls/{resolution}/{segment}"
        return FileResponse(open(segment_path, 'rb'), content_type="video/MP2T")
    except (Video.DoesNotExist, FileNotFoundError):
        raise Http404()
