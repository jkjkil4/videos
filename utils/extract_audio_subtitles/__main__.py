import argparse
import io
import json
import math
import subprocess
import wave
from collections.abc import Generator, Iterable
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

from vosk import KaldiRecognizer, Model, SetLogLevel

SetLogLevel(-1)


class SubtitleItem(TypedDict):
    conf: float
    end: float
    start: float
    word: str


def load_wave(file_path: str) -> wave.Wave_read:
    """
    将输入音频转成 Vosk 需要的单声道 16kHz WAV 并返回 wave 对象。
    """
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-ac', '1',
        '-ar', '16000',
        '-sample_fmt', 's16',
        '-f', 'wav',
        '-'  # 输出到 stdout
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    wav_bytes = proc.stdout.read()
    proc.wait()
    return wave.open(io.BytesIO(wav_bytes), 'rb')


@lru_cache(maxsize=1)
def get_model() -> Model:
    root = Path(__file__).resolve().parent
    return Model(str(root / 'vosk-models' / 'vosk-model-small-cn-0.22'))


def wave_to_subtitles(wf: wave.Wave_read) -> Generator[SubtitleItem, None, None]:
    """
    识别 wave 音频并返回逐词时间戳列表。
    """
    rec = KaldiRecognizer(get_model(), wf.getframerate())
    rec.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if 'result' in res:
                yield from res['result']

    # 最后一段
    res = json.loads(rec.FinalResult())
    if 'result' in res:
        yield from res['result']


def print_subtitles(subtitles: Iterable[SubtitleItem]) -> None:
    """
    按指定格式逐行打印识别结果。
    """
    for subtitle in subtitles:
        word = subtitle['word']
        start = math.floor(subtitle['start'] * 100) / 100
        end = math.ceil(subtitle['end'] * 100) / 100
        conf = subtitle['conf']
        print(f'word: {word}\t range: {start:.2f} ~ {end:.2f}\t conf: {conf:.3f}')


def main(file_path: str) -> None:
    wf = load_wave(file_path)
    print_subtitles(wave_to_subtitles(wf))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='输入音频文件路径，例如 test.wav')
    args = parser.parse_args()
    main(args.file_path)
