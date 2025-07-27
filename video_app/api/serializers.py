"""
video_app.api.serializers
~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the serializer for the Video model used in API responses.
"""

from rest_framework import serializers
from video_app.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializes the Video model with an additional field for
    absolute thumbnail URL generation.
    """
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'created_at',
            'title',
            'description',
            'thumbnail_url',
            'category'
        ]

    def get_thumbnail_url(self, obj):
        """
        Returns an absolute URL to the video's thumbnail image.

        Args:
            obj (Video): The video instance.

        Returns:
            str: Absolute URL of the thumbnail.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail.url)
