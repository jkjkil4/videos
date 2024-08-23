from pprint import pprint

from janim.imports import *
from janim.render.writer import AudioWriter, VideoWriter

folder_path = '2024/LearnOpenGL-Videos/videos'
output_path = '2024/LearnOpenGL-Videos/heavy_watermark'


def create_timeline_class_by_file(filename: str) -> type[Timeline]:
    def construct(self: Timeline) -> None:
        file = os.path.join(folder_path, filename)

        audio = Audio(file)
        video = Video(file).show()
        Text('jkjkil-jiang\nPreview', font_size=80, fill_alpha=0.1).show()

        self.play_audio(audio)
        video.start()
        self.forward(audio.duration())

    return type(
        filename.rstrip('.mp4'),
        (Timeline,),
        dict(
            CONFIG=Config(
                pixel_width=960,
                pixel_height=540,
                audio_channels=2
            ),
            construct=construct
        )
    )


for filename in os.listdir(folder_path):
    if not filename.endswith('.mp4'):
        continue
    if os.path.exists(os.path.join(output_path, filename)):
        continue

    cls = create_timeline_class_by_file(filename)
    anim = cls().build()

    # from janim.gui.anim_viewer import AnimViewer
    # AnimViewer.views(anim)
    # return

    file = os.path.join(output_path, filename)

    video_file = file + '.mp4'
    VideoWriter.writes(anim, video_file)

    audio_file = file + '.mp3'
    AudioWriter.writes(anim, audio_file)

    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-shortest',
        '-c:v', 'copy',
        '-c:a', 'aac',
        file
    ]
    pprint(command)
    with sp.Popen(command) as process:
        process.wait()
