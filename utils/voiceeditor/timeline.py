import os
import subprocess as sp

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFileDialog
from utils.shared.timeline import SAMPLE_RATE, Timeline as BaseTimeline


class Timeline(BaseTimeline):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_number = 1

    def set_start_number(self, number: int) -> None:
        self.start_number = number
        self.update()

    def export(self) -> None:
        if not self.has_audio():
            return

        dir_path = QFileDialog.getExistingDirectory(self, '导出音频')
        if not dir_path:
            return

        indices = [round(t * SAMPLE_RATE) for t in self.cut_ranges.get_boundaries()]
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

            with sp.Popen(command, stdin=sp.PIPE) as writing_process:
                writing_process.stdin.write(self.samples[indices[i * 2]:indices[i * 2 + 1]])

            print('已导出', file_path)

    def paint_others(self, event, p: QPainter):
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(Qt.GlobalColor.white)

        cut_ranges = self.cut_ranges.get_ranges()
        draw_start = not cut_ranges or cut_ranges[0][0] != 0
        number = self.start_number

        if draw_start:
            p.drawText(QPointF(self.t_to_pixel(0), 12), str(number))
            number += 1

        for _, cut_end in cut_ranges:
            if cut_end == self.max_t:
                continue
            p.drawText(QPointF(self.t_to_pixel(cut_end), 12), str(number))
            number += 1
