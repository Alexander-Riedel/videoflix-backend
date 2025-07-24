# import subprocess
import ffmpeg


# def convert_480p(source):
#     target = source + '_480p.mp4'
#     cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#     subprocess.run(cmd)

def convert_480p(source):
    target = source.replace('.mp4', '_480p.mp4')
    (
        ffmpeg
        .input(source)
        .filter('scale', 854, 480)       # HD-480 ist 854×480
        .output(target,
                vcodec='libx264',
                crf=23,
                acodec='aac',
                strict='-2')
        .run(overwrite_output=True)      # überschreibt ggf. existierende Ziel-Datei
    )