import ffmpeg

def convert_to_hls(source: str):
    """
    Erzeugt aus source.mp4 eine HLS-Playlist source.m3u8
    mit copy-Codec und 10-Sekunden-Segmenten.
    """
    target = source.replace('.mp4', '.m3u8')
    (
        ffmpeg
        .input(source)
        .output(
            target,
            vcodec='copy',        # kein Re-Encoding Video
            acodec='copy',        # kein Re-Encoding Audio
            start_number=0,       # erste Segment-Nummer
            hls_time=10,          # Länge jedes Segments in Sekunden
            hls_list_size=0,      # alle Segmente in Playlist
            f='hls'               # Format HLS
        )
        .run(overwrite_output=True)
    )
