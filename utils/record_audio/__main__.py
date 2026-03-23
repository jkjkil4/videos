import argparse
import time
import wave
from pathlib import Path

import sounddevice as sd
from pyrnnoise import RNNoise

try:
    import msvcrt
except ImportError:
    msvcrt = None


def main(output_path: str) -> None:
    sample_rate = 48000
    channels = 1
    block_size = 1024

    orig_file = Path(output_path + '_orig.wav')
    orig_file.parent.mkdir(parents=True, exist_ok=True)

    output_file = Path(output_path + '.wav')

    frames: list[bytes] = []
    error_points: list[float] = []
    if msvcrt is not None:
        print('开始录音，按空格记录 ERROR Point，按 Ctrl+C 停止...')
    else:
        print('开始录音，按 Ctrl+C 停止...')

    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype='int16',
            blocksize=block_size,
        ) as stream:
            start_time = time.perf_counter()
            while True:
                data, _ = stream.read(block_size)
                frames.append(data.tobytes())
                if msvcrt is not None:
                    while msvcrt.kbhit():
                        if msvcrt.getwch() == ' ':
                            point = round(time.perf_counter() - start_time, 2)
                            error_points.append(point)
                            print(f'记录 ERROR Point: {point:.2f}s')
    except KeyboardInterrupt:
        pass

    with wave.open(str(orig_file), 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    denoiser = RNNoise(48000)
    for _ in denoiser.denoise_wav(orig_file, output_file):
        pass

    print(f'录音已保存到: {output_file}')
    if error_points:
        error_file = Path(output_path + '_errors.txt')
        error_file.write_text(','.join(f'{point:.2f}' for point in error_points), encoding='utf-8')
        print(f'ERROR Points 已保存到: {error_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='录制音频并保存为 WAV 文件')
    parser.add_argument('output_path', help='输出 WAV 文件（不含后缀），例如 output')
    args = parser.parse_args()
    main(args.output_path)
