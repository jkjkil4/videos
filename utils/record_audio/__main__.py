import argparse
import wave
from pathlib import Path

import sounddevice as sd


def main(output_path: str) -> None:
    sample_rate = 16000
    channels = 1
    block_size = 1024
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    frames: list[bytes] = []
    print('开始录音，按 Ctrl+C 停止...')

    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype='int16',
            blocksize=block_size,
        ) as stream:
            while True:
                data, _ = stream.read(block_size)
                frames.append(data.tobytes())
    except KeyboardInterrupt:
        pass

    with wave.open(str(output_file), 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f'录音已保存到: {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='录制音频并保存为 WAV 文件')
    parser.add_argument('output_path', help='输出 WAV 文件路径，例如 output.wav')
    args = parser.parse_args()
    main(args.output_path)
