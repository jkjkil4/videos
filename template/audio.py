import json
import os
from functools import lru_cache
from typing import TypedDict

from janim.utils.file_ops import find_file
from janim.items.audio import Audio
from janim.anims.timeline import Timeline


class SubtitleItem(TypedDict):
    text: str
    range: list[float]
    contains_math: bool


SubtitleJson = list[SubtitleItem]


@lru_cache(maxsize=None)
def _read_subtitle_json(resolved_path: str, mtime: float) -> SubtitleJson:
    with open(resolved_path, encoding='utf-8') as file:
        return json.load(file)


def read_subtitle_json(file_path: str) -> SubtitleJson:
    resolved_path = find_file(file_path)
    mtime = os.path.getmtime(resolved_path)
    return _read_subtitle_json(resolved_path, mtime)


def read_audio_with_subtitles(file_path: str, begin: float, end: float) -> tuple[Audio, SubtitleJson]:
    audio = Audio(file_path, begin, end)
    subtitles = [
        item
        for item in read_subtitle_json(os.path.splitext(audio.file_path)[0] + '.json')
        if item['range'][0] >= begin and item['range'][1] <= end
    ]
    return (audio, subtitles)


def play_audio_with_subtitles(
    timeline: Timeline,
    file_path: str,
    begin: float,
    end: float,
    *,
    delay: float = 0,
    mul: float = 1,
) -> None:
    audio, subtitles = read_audio_with_subtitles(file_path, begin, end)
    if mul != 1:
        audio.mul(mul)
    timeline.play_audio(audio, delay=delay)
    for s in subtitles:
        sbegin, send = s['range']
        sduration = send - sbegin
        timeline.subtitle(
            s['text'],
            delay=delay + (sbegin - begin),
            duration=sduration,
            use_typst_text=s['contains_math']
        )
