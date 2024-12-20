import math
import os
import subprocess as sp
from bisect import bisect_left, bisect_right
from dataclasses import dataclass

import numpy as np
from janim.gui.audio_player import AudioPlayer
from janim.gui.precise_timer import PreciseTimer
from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (QColor, QKeyEvent, QMouseEvent, QPainter,
                           QPainterPath, QPen)
from PySide6.QtWidgets import QFileDialog, QWidget

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
    '''
    记录按键状态
    '''
    w: bool = False
    a: bool = False
    s: bool = False
    d: bool = False


@dataclass
class Chart:
    '''
    缓存波形图预览数据
    '''
    data: np.ndarray
    unit: int

    def __init__(self, samples: np.ndarray, unit: int):
        self.data: np.ndarray = np.max(
            np.abs(
                samples[:len(samples) // unit * unit].max(axis=1).reshape(-1, unit)
            ),
            axis=1
        ) / np.iinfo(np.int16).max

        self.unit = unit

    def t_to_n(self, t: float) -> int:
        return int(t * SAMPLE_RATE / self.unit)

    def n_to_t(self, n: int) -> float:
        return n * self.unit / SAMPLE_RATE


class Timeline(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.is_pressing = Pressing()
        self.start_number = 1
        self.set_samples(np.empty((0, 2)))

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

    def set_samples(self, samples: np.ndarray) -> None:
        self.samples = samples
        self.range = TimeRange(-0.5, 6)
        self.chart_cache: dict[int, Chart] = {}
        self.gaps: list[float] = []
        self.progress = 0
        self.max_t = len(samples) / SAMPLE_RATE
        self.max_progress = int(self.max_t * FPS)

    def set_start_number(self, number: int) -> None:
        self.start_number = number
        self.update()

    def export(self) -> None:
        dir_path = QFileDialog.getExistingDirectory(self, '导出音频')
        if not dir_path:
            return

        indices = [round(gap * SAMPLE_RATE) for gap in self.gaps]
        if indices and indices[0] == 0:
            indices.pop(0)
        else:
            indices.insert(0, 0)

        if indices and indices[-1] == len(self.samples):
            indices.pop()
        else:
            indices.append(len(self.samples))

        for i in range(len(indices) // 2):
            file_path = os.path.join(dir_path, f'{self.start_number + i}.mp3')
            command = [
                'ffmpeg',
                '-y',   # overwrite output file if it exists
                '-f', 's16le',
                '-ar', str(SAMPLE_RATE),      # framerate & samplerate
                '-ac', '2',
                '-i', '-',
                '-loglevel', 'error',
                file_path
            ]

            with sp.Popen(command, stdin=sp.PIPE) as writring_process:
                writring_process.stdin.write(self.samples[indices[i * 2]:indices[i * 2 + 1]])

            print('已导出', file_path)

    def t_to_pixel(self, t: float) -> float:
        return (t - self.range.at) / self.range.duration * self.width()

    def pixel_to_t(self, x: float) -> float:
        return x / self.width() * self.range.duration + self.range.at

    def get_current_chart(self) -> Chart:
        unit = max(1000,
                   min(len(self.samples) // CHART_SAMPLES,
                       int(self.range.duration * SAMPLE_RATE / CHART_SAMPLES // 1000 * 1000)))
        cache = self.chart_cache.get(unit, None)
        if cache is not None:
            return cache

        chart = Chart(self.samples, unit)
        self.chart_cache[unit] = chart
        return chart

    def set_progress(self, progress: int) -> None:
        progress = max(0, min(self.max_progress, progress))
        if progress == self.progress:
            return False

        self.progress = progress

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
        start, end = max(0, min(self.max_t, *self.modify_range)), min(self.max_t, max(0, *self.modify_range))
        if start == end:
            return

        left = bisect_left(self.gaps, start)
        right = bisect_right(self.gaps, end)
        is_selection = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)

        orig_left_is_selection = left % 2 == 1
        orig_right_is_selection = right % 2 == 1

        if orig_left_is_selection and orig_right_is_selection:
            if is_selection:
                self.gaps = [*self.gaps[:left], *self.gaps[right:]]
            else:
                self.gaps = [*self.gaps[:left], start, end, *self.gaps[right:]]
        elif not orig_left_is_selection and orig_right_is_selection:
            if is_selection:
                self.gaps = [*self.gaps[:left], start, *self.gaps[right:]]
            else:
                self.gaps = [*self.gaps[:left], end, *self.gaps[right:]]
        elif orig_left_is_selection and not orig_right_is_selection:
            if is_selection:
                self.gaps = [*self.gaps[:left], end, *self.gaps[right:]]
            else:
                self.gaps = [*self.gaps[:left], start, *self.gaps[right:]]
        else:   # not and not
            if is_selection:
                self.gaps = [*self.gaps[:left], start, end, *self.gaps[right:]]
            else:
                self.gaps = [*self.gaps[:left], *self.gaps[right:]]

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
            scale_factor = 0.97**scale_factor_pow

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
        if self.set_progress(self.progress + 1):
            left = math.floor(self.progress / FPS * SAMPLE_RATE)
            right = math.floor((self.progress + 1) / FPS * SAMPLE_RATE)
            self.audio_player.write(self.samples[left:right].tobytes())
        else:
            self.audio_timer.stop()

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
                QPointF(
                    pixel,
                    self.height() * (0.95 - 0.9 * chart.data[n])
                )
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
        for i in range(len(self.gaps) // 2):
            p.drawRect(QRectF(QPointF(self.t_to_pixel(self.gaps[i * 2]), 0),
                              QPointF(self.t_to_pixel(self.gaps[i * 2 + 1]), self.height())))

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

        # 绘制区段编号文本
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(Qt.GlobalColor.white)
        draw_start = not self.gaps or self.gaps[0] != 0
        number = self.start_number
        if draw_start:
            p.drawText(QPointF(self.t_to_pixel(0), 12), str(number))
            number += 1
        for i in range(len(self.gaps) // 2):
            t = self.gaps[i * 2 + 1]
            if t == self.max_t:
                continue
            p.drawText(QPointF(self.t_to_pixel(t), 12), str(number))
            number += 1

        # 绘制边框
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(41, 171, 202) if self.hasFocus() else QColor(28, 117, 138), 3))
        p.drawRect(self.rect())
