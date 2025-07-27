import os
import ffmpeg


def convert_to_hls(source: str):
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