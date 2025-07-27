"""
video_app.tasks
~~~~~~~~~~~~~~~

This module provides background tasks related to video processing.

The main task converts uploaded MP4 videos into segmented HLS format
(HTTP Live Streaming) in multiple resolutions using ffmpeg.
"""

import os
import ffmpeg


def convert_to_hls(source: str):
    """
    Converts an uploaded MP4 video into HLS format with multiple resolutions.

    Args:
        source (str): The full path to the source MP4 video file.

    Output:
        Creates directories for 480p, 720p, and 1080p containing:
        - index.m3u8 manifest
        - .ts segments for each resolution
    """
    resolutions = {
        '480p': '854x480',
        '720p': '1280x720',
        '1080p': '1920x1080',
    }

    base_name = os.path.splitext(os.path.basename(source))[0]
    output_dir = os.path.join(os.path.dirname(source), base_name + '_hls')
    os.makedirs(output_dir, exist_ok=True)

    for res, size in resolutions.items():
        res_dir = os.path.join(output_dir, res)
        os.makedirs(res_dir, exist_ok=True)

        out_playlist = os.path.join(res_dir, 'index.m3u8')
        out_segments = os.path.join(res_dir, f'{res}%d.ts')

        (
            ffmpeg
            .input(source)
            .output(
                out_playlist,
                vf=f'scale={size}',
                acodec='aac',
                vcodec='h264',
                hls_time=10,
                hls_list_size=0,
                start_number=0,
                f='hls',
                hls_segment_filename=out_segments
            )
            .run(overwrite_output=True)
        )
