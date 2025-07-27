"""
video_app.api.views
~~~~~~~~~~~~~~~~~~~

This module provides API endpoints for listing videos, 
streaming HLS playlists (m3u8), and individual video segments (ts files).

All endpoints require JWT-based authentication.
"""

import os
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from video_app.models import Video


class VideoListView(APIView):
    """
    Returns a list of available videos with metadata and thumbnail URLs.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all()
        data = [
            {
                "id": video.id,
                "created_at": video.created_at,
                "title": video.title,
                "description": video.description,
                "thumbnail_url": request.build_absolute_uri(video.thumbnail.url),
                "category": video.category
            }
            for video in videos
        ]
        return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_m3u8(request, movie_id, resolution):
    """
    Streams the HLS master playlist (.m3u8) for a given video and resolution.

    Args:
        movie_id (int): ID of the video.
        resolution (str): Resolution folder (e.g. '480p').

    Returns:
        FileResponse: .m3u8 file response with correct content type.
    Raises:
        Http404: If video or HLS file is not found.
    """
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
    """
    Streams a single HLS video segment (.ts file) for a given video and resolution.

    Args:
        movie_id (int): ID of the video.
        resolution (str): Resolution folder (e.g. '480p').
        segment (str): Filename of the segment (e.g. '000.ts').

    Returns:
        FileResponse: Binary .ts file stream.
    Raises:
        Http404: If video or segment file is not found.
    """
    try:
        video = Video.objects.get(pk=movie_id)
        base = os.path.splitext(video.video.path)[0]
        segment_path = f"{base}_hls/{resolution}/{segment}"
        return FileResponse(open(segment_path, 'rb'), content_type="video/MP2T")
    except (Video.DoesNotExist, FileNotFoundError):
        raise Http404()
