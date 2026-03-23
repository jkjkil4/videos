import math
import os
import subprocess as sp
from dataclasses import dataclass

import numpy as np
from utils.shared.cut_range import CutRangeCollection
from janim.gui.utils.audio_player import AudioPlayer
from janim.gui.utils.precise_timer import PreciseTimer
from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (QColor, QKeyEvent, QMouseEvent, QPainter,
                           QPainterPath, QPen)
from PySide6.QtWidgets import QWidget

CHART_SAMPLES = 500
SAMPLE_RATE = 44100
FPS = 30
PLAYBACK_SPACING = 40


@dataclass
class TimeRange:
    at: float
    duration: float

    @property
    def end(self) -> float:
        return self.at + self.duration


@dataclass
class Pressing:
    w: bool = False
    a: bool = False
    s: bool = False
    d: bool = False


@dataclass
class Chart:
    data: np.ndarray
    unit: int

    def __init__(self, samples: np.ndarray, unit: int):
        if len(samples) < unit:
            self.data = np.array([0.0], dtype=np.float32)
        else:
            trimmed = samples[:len(samples) // unit * unit]
            channel_max = np.max(np.abs(trimmed), axis=1)
            self.data = np.max(channel_max.reshape(-1, unit), axis=1) / np.iinfo(np.int16).max

        self.unit = unit

    def t_to_n(self, t: float) -> int:
        return int(t * SAMPLE_RATE / self.unit)

    def n_to_t(self, n: int) -> float:
        return n * self.unit / SAMPLE_RATE


class Timeline(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.is_pressing = Pressing()
        self.samples = np.empty((0, 2), dtype=np.int16)
        self.range = TimeRange(-0.5, 6)
        self.chart_cache: dict[int, Chart] = {}
        self.cut_ranges = CutRangeCollection()
        self.progress = 0
        self.max_t = 0.0
        self.max_progress = 0

        self.key_timer = QTimer(self)
        self.key_timer.timeout.connect(self.on_key_timer_timeout)
        self.key_timer.start(20)

        self.audio_timer = PreciseTimer(1 / FPS, self)
        self.audio_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.audio_timer.timeout.connect(self.on_audio_timer_timeout)
        self.audio_player = AudioPlayer(SAMPLE_RATE, 2, FPS)

        self.modify_range: tuple[float, float] | None = None
        self.press_modifier: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def has_audio(self) -> bool:
        return len(self.samples) > 0

    def set_samples(self, samples: np.ndarray) -> None:
        self.audio_timer.stop()
        self.samples = samples
        self.range = TimeRange(-0.5, 6)
        self.chart_cache = {}
        self.cut_ranges.clear()
        self.progress = 0
        self.max_t = len(samples) / SAMPLE_RATE
        self.max_progress = int(self.max_t * FPS)
        self.update()

    def t_to_pixel(self, t: float) -> float:
        if self.width() == 0:
            return 0
        return (t - self.range.at) / self.range.duration * self.width()

    def pixel_to_t(self, x: float) -> float:
        if self.width() == 0:
            return 0
        return x / self.width() * self.range.duration + self.range.at

    def get_current_chart(self) -> Chart:
        if len(self.samples) == 0:
            return Chart(np.zeros((1000, 2), dtype=np.int16), 1000)

        unit = max(
            1000,
            min(
                len(self.samples) // CHART_SAMPLES,
                int(self.range.duration * SAMPLE_RATE / CHART_SAMPLES // 1000 * 1000)
            )
        )
        cache = self.chart_cache.get(unit)
        if cache is not None:
            return cache

        chart = Chart(self.samples, unit)
        self.chart_cache[unit] = chart
        return chart

    def set_progress(self, progress: int) -> bool:
        progress = max(0, min(self.max_progress, progress))
        if progress == self.progress:
            return False

        self.progress = progress

        if self.width() > 0:
            space = PLAYBACK_SPACING / self.width() * self.range.duration
            pgt = progress / FPS
            pixel = self.t_to_pixel(pgt)
            if pixel < PLAYBACK_SPACING:
                self.range.at = pgt - space
            if pixel > self.width() - PLAYBACK_SPACING:
                self.range.at = pgt + space - self.range.duration

        self.update()
        return True

    def drag_progress(self, event: QMouseEvent) -> None:
        self.audio_timer.stop()
        self.set_progress(int(self.pixel_to_t(event.position().x()) * FPS))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.press_modifier = event.modifiers()
            t = self.pixel_to_t(event.position().x())

            if self.press_modifier & (Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier):
                self.modify_range = (t, t)
                self.update()
            else:
                self.drag_progress(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton:
            t = self.pixel_to_t(event.position().x())

            if self.modify_range is not None:
                self.modify_range = (self.modify_range[0], t)
                self.update()
            else:
                self.drag_progress(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return

        if self.modify_range is not None:
            self.on_mouse_selection(event)

    def on_mouse_selection(self, event: QMouseEvent) -> None:
        start = max(0, min(self.max_t, *self.modify_range))
        end = min(self.max_t, max(0, *self.modify_range))
        if start == end:
            self.modify_range = None
            self.update()
            return

        is_cut_selection = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        self.cut_ranges.modify(start, end, is_cut_selection)

        self.modify_range = None
        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()

        if key == Qt.Key.Key_W:
            self.is_pressing.w = True
        elif key == Qt.Key.Key_A:
            self.is_pressing.a = True
        elif key == Qt.Key.Key_S:
            self.is_pressing.s = True
        elif key == Qt.Key.Key_D:
            self.is_pressing.d = True

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        key = event.key()

        if key == Qt.Key.Key_W:
            self.is_pressing.w = False
        elif key == Qt.Key.Key_A:
            self.is_pressing.a = False
        elif key == Qt.Key.Key_S:
            self.is_pressing.s = False
        elif key == Qt.Key.Key_D:
            self.is_pressing.d = False
        elif key == Qt.Key.Key_Space:
            if self.audio_timer.isActive():
                self.audio_timer.stop()
            else:
                self.audio_timer.start_precise_timer()

    def on_key_timer_timeout(self) -> None:
        scale_factor_pow = self.is_pressing.w - self.is_pressing.s
        if scale_factor_pow != 0:
            scale_factor = 0.97 ** scale_factor_pow
            half = self.range.duration / 2
            mid = self.range.at + half
            self.range.at = mid - half * scale_factor
            self.range.duration = self.range.duration * scale_factor
            self.update()

        shift_dir = self.is_pressing.d - self.is_pressing.a
        if shift_dir != 0:
            shift = self.range.duration * 0.05 * shift_dir
            self.range.at += shift
            self.update()

    def on_audio_timer_timeout(self) -> None:
        if not self.has_audio():
            self.audio_timer.stop()
            return

        if self.set_progress(self.progress + 1):
            left = math.floor(self.progress / FPS * SAMPLE_RATE)
            right = math.floor((self.progress + 1) / FPS * SAMPLE_RATE)
            self.audio_player.write(self.samples[left:right].tobytes())
        else:
            self.audio_timer.stop()

    def get_processed_samples(self) -> np.ndarray:
        if not self.has_audio() or not self.cut_ranges.has_ranges():
            return self.samples

        intervals: list[tuple[int, int]] = []
        start_idx = 0

        for cut_start_t, cut_end_t in self.cut_ranges.get_ranges():
            cut_start = max(0, min(len(self.samples), round(cut_start_t * SAMPLE_RATE)))
            cut_end = max(0, min(len(self.samples), round(cut_end_t * SAMPLE_RATE)))
            if cut_start > start_idx:
                intervals.append((start_idx, cut_start))
            start_idx = max(start_idx, cut_end)

        if start_idx < len(self.samples):
            intervals.append((start_idx, len(self.samples)))

        if not intervals:
            return np.empty((0, 2), dtype=np.int16)

        return np.concatenate([self.samples[left:right] for left, right in intervals], axis=0)

    def export(self, file_path: str) -> None:
        if not self.has_audio() or not file_path:
            return

        output_samples = self.get_processed_samples()
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        command = [
            'ffmpeg',
            '-y',
            '-f', 's16le',
            '-ar', str(SAMPLE_RATE),
            '-ac', '2',
            '-i', '-',
            '-loglevel', 'error',
            file_path,
        ]

        with sp.Popen(command, stdin=sp.PIPE) as writing_process:
            if writing_process.stdin is not None:
                writing_process.stdin.write(output_samples.tobytes())

    def focusInEvent(self, event):
        self.update()

    def focusOutEvent(self, event):
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制波形图
        chart = self.get_current_chart()
        n_start = max(0, chart.t_to_n(self.range.at))
        n_end = min(len(chart.data) - 1, chart.t_to_n(self.range.end))
        if n_end > n_start:
            pixel_start = self.t_to_pixel(chart.n_to_t(n_start))
            pixel_end = self.t_to_pixel(chart.n_to_t(n_end))
            points = [
                QPointF(pixel, self.height() * (0.95 - 0.9 * chart.data[n]))
                for pixel, n in zip(np.linspace(pixel_start, pixel_end, n_end - n_start), range(n_start, n_end))
            ]
            if len(points) >= 2:
                path = QPainterPath()
                path.moveTo(points[0])
                for point in points[1:]:
                    path.lineTo(point)
                path.lineTo(QPointF(point.x(), self.height()))
                path.lineTo(QPointF(points[0].x(), self.height()))
                path.closeSubpath()

                p.setBrush(QColor(59, 135, 115))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawPath(path)

        # 绘制剔除部分
        p.setBrush(QColor(200, 128, 128, 128))
        p.setPen(Qt.PenStyle.NoPen)
        for cut_start, cut_end in self.cut_ranges.get_ranges():
            p.drawRect(
                QRectF(
                    QPointF(self.t_to_pixel(cut_start), 0),
                    QPointF(self.t_to_pixel(cut_end), self.height()),
                )
            )

        # 绘制选中区域
        if self.modify_range is not None:
            start, end = map(self.t_to_pixel, self.modify_range)
            p.setBrush(QColor(255, 255, 255, 128))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRect(QRectF(QPointF(start, 0), QPointF(end, self.height())))

        # 绘制进度条
        x = self.t_to_pixel(self.progress / FPS)
        p.setBrush(Qt.GlobalColor.white)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(QRectF(x - 1, 0, 2, self.height()))

        # 绘制其它
        self.paint_others(event, p)

        # 绘制边框
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(41, 171, 202) if self.hasFocus() else QColor(28, 117, 138), 3))
        p.drawRect(self.rect())

    def paint_others(self, event, p: QPainter):
        pass
