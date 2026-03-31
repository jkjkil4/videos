import json
import os
import types
from functools import lru_cache
from typing import NotRequired, TypedDict

from janim.anims.animation import TimeRange
from janim.anims.timeline import Timeline
from janim.items.audio import Audio
from janim.utils.file_ops import find_file


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
) -> TimeRange:
    audio, subtitles = read_audio_with_subtitles(file_path, begin, end)
    if mul != 1:
        audio.mul(mul)
    t = timeline.play_audio(audio, delay=delay)
    for s in subtitles:
        sbegin, send = s['range']
        sduration = send - sbegin
        timeline.subtitle(
            s['text'],
            delay=delay + (sbegin - begin),
            duration=sduration,
            use_typst_text=s['contains_math']
        )
    return t


class SeqEntry(TypedDict):
    file: NotRequired[str | types.EllipsisType]
    begin: float
    end: float
    delay: NotRequired[float]
    mul: NotRequired[float | types.EllipsisType]


def seq_play_audio_with_subtitles(
    timeline: Timeline,
    entries: list[SeqEntry]
) -> list[TimeRange]:
    """
    示例：

    .. code-block:: python

        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_11_4.wav', 'begin': 0, 'end': 66.5, 'delay': 0.5, 'mul': 1.25 },
                { 'file': ..., 'begin': 66.5, 'end': 74, 'delay': 1, 'mul': ... },
                { 'file': 'audio_11_5.wav', 'begin': 0, 'end': 32.2, 'delay': 0.5, 'mul': 1.25 },
                { 'file': ..., 'begin': 32.2, 'end': 45.2, 'delay': 1, 'mul': ... },
                { 'file': ..., 'begin': 54.2, 'end': 70, 'delay': 1.5, 'mul': ... },
            ]
        )
    """
    global_delay = 0
    last_file: str | None = None
    last_mul = 1.0

    ranges: list[TimeRange] = []

    for entry in entries:
        raw_file = entry.get('file')
        if raw_file is None:
            assert last_file is not None, 'Missing file in first seq entry'
            file_path = last_file
        elif raw_file is ...:
            assert last_file is not None, 'Cannot use ellipsis for file in first seq entry'
            file_path = last_file
        else:
            file_path = raw_file

        raw_mul = entry.get('mul')
        if raw_mul is None:
            mul = 1
        elif raw_mul is ...:
            mul = last_mul
        else:
            mul = raw_mul

        delay = global_delay + entry.get('delay', 0)
        t = play_audio_with_subtitles(
            timeline,
            file_path,
            entry['begin'],
            entry['end'],
            delay=delay,
            mul=mul
        )
        ranges.append(t)
        last_file = file_path
        last_mul = mul
        duration = entry['end'] - entry['begin']
        global_delay = delay + duration

    return ranges
