import numpy as np
from janim.imports import *
from scipy.interpolate import interp1d
from scipy.signal import stft

# file = R'D:\SteamLibrary\steamapps\music\Rabi-Ribi - Original Soundtrack\FLAC\Rabi-Ribi Original Soundtrack - 32 Forgotten Cave II.flac'
# file = R'D:\SteamLibrary\steamapps\music\Rabi-Ribi - Original Soundtrack\FLAC\Rabi-Ribi Original Soundtrack - 43 M.R..flac'
file = R'D:\SteamLibrary\steamapps\music\Rabi-Ribi - Original Soundtrack\FLAC\Rabi-Ribi Original Soundtrack - 52 Nightwalker.flac'
# file = R'D:\SteamLibrary\steamapps\music\Rabi-Ribi - Original Soundtrack\FLAC\Rabi-Ribi Original Soundtrack - 49 Game Over.flac'
# file = R'D:\SteamLibrary\steamapps\music\Rabi-Ribi - Original Soundtrack\FLAC\Rabi-Ribi Original Soundtrack - 13 Spectral Cave.flac'
# file = R'D:\SteamLibrary\steamapps\music\Rabi-Ribi - Original Soundtrack\FLAC\Rabi-Ribi Original Soundtrack - 09 Rabi Rabi Ravine Ver.2.flac'


class AudioVisualizer(Timeline):
    CONFIG = Config(
        preview_fps=40,
        background_color=Color('white')
    )

    def construct(self) -> None:
        # 可配置的一些参数
        N = 24
        MARGIN = DEFAULT_ITEM_TO_EDGE_BUFF      # 与屏幕的边距
        SPACING = DEFAULT_ITEM_TO_ITEM_BUFF     # 矩形之间的横向间距
        MAX_HEIGHT = Config.get.frame_height - 2 * MARGIN   # 矩形的最大高度
        DB_MIN = 25     # 最小 db，大于这个才有高度
        DB_MAX = 50     # 最大 db，超过这个会顶到最上端

        # 载入音频
        audio = Audio(file)

        # FFT
        fs = Config.get.audio_framerate
        data = np.max(np.abs(audio._samples.data), axis=1)
        f, t, Zxx = stft(data, fs=fs, nperseg=fs // 20, noverlap=0)

        # FFT 会得到频率达到几万的，不需要那么多，这里取最高到 fs // 4 的频率
        idx = bisect(f, fs // 4)
        f = f[:idx]
        Zxx = Zxx[:idx, :]

        # 转为振幅并取对数
        # 我不确定这里的 db 是否真的可以表示“分贝”的含义，能用就行（）
        magnitude = np.abs(Zxx)
        db = 20 * np.log10(magnitude + 1e-6)

        # 分块求均值
        f_per_block = len(db) // N
        db_blocks = [
            np.clip(
                np.mean(
                    db[i * f_per_block: (i + 1) * f_per_block, :],
                    axis=0
                ),
                DB_MIN, DB_MAX
            )
            for i in range(0, N)
        ]

        # 创建矩形
        width = (Config.get.frame_width - 2 * MARGIN - (N - 1) * SPACING) / N
        rect = Rect(width, stroke_alpha=0, fill_alpha=1, color='#e4e4e4')
        rects = rect * N
        rects.points.arrange(buff=SPACING).to_border(DOWN, buff=MARGIN)

        # 构造动画
        anims = []
        for block, rect in zip(db_blocks, rects):
            interp = interp1d(t, block)     # 线性插值

            def updater(data: Rect, p: UpdaterParams, interp=interp):
                y = interp(p.global_t)
                height = (y - DB_MIN) / (DB_MAX - DB_MIN) * MAX_HEIGHT
                data.points.set_height(height, stretch=True, about_edge=DOWN)

            anims.append(DataUpdater(rect, updater))

        # 播放
        self.play_audio(audio)
        self.play(*anims, duration=audio.duration())
