import subprocess as sp

import numpy as np
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QMessageBox,
                               QPushButton, QVBoxLayout, QWidget)
from utils.shared.timeline import SAMPLE_RATE, Timeline


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.current_file_path = ''

        self.setup_ui()
        self.bind_signals()

        self.setWindowTitle('Audio Clip')
        self.resize(1000, 200)
        self.timeline.setFocus()

    def setup_ui(self) -> None:
        self.timeline = Timeline()
        self.timeline.setMinimumHeight(120)

        self.tip = QLabel('操作: 左键拖动=定位播放; Shift+左键拖动=标记剔除; Ctrl+左键拖动=取消剔除; Space=播放/暂停; W/S=缩放; A/D=平移')

        self.btn_open = QPushButton('打开音频')
        self.btn_export = QPushButton('导出剔除后音频')

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addStretch()

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.timeline, 1)
        bottom_layout.addLayout(btn_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tip)
        main_layout.addLayout(bottom_layout, 1)
        self.setLayout(main_layout)

    def bind_signals(self) -> None:
        self.btn_open.clicked.connect(self.on_btn_open_clicked)
        self.btn_export.clicked.connect(self.on_btn_export_clicked)

    def on_btn_open_clicked(self) -> None:
        file_path = QFileDialog.getOpenFileName(self, '打开音频')[0]
        if not file_path:
            return

        self.current_file_path = file_path
        command = [
            'ffmpeg',
            '-vn',
            '-i', file_path,
            '-f', 's16le',
            '-acodec', 'pcm_s16le',
            '-ar', str(SAMPLE_RATE),
            '-ac', '2',
            '-loglevel', 'error',
            '-',
        ]

        with sp.Popen(command, stdout=sp.PIPE) as reading_process:
            if reading_process.stdout is None:
                return
            data = np.frombuffer(reading_process.stdout.read(), dtype=np.int16)

        if len(data) == 0:
            self.timeline.set_samples(np.empty((0, 2), dtype=np.int16))
            return

        data = data[: len(data) // 2 * 2].reshape((-1, 2))
        self.timeline.set_samples(data)

    def on_btn_export_clicked(self) -> None:
        if not self.timeline.has_audio():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '导出剔除后音频',
            self.suggest_output_path(),
            'Audio Files (*.wav *.mp3 *.flac *.m4a);;All Files (*)',
        )
        if not file_path:
            return

        self.timeline.export(file_path)
        QMessageBox.information(self, '提示', f'已导出到文件 {file_path}')

    def suggest_output_path(self) -> str:
        if not self.current_file_path:
            return 'output.wav'

        dot = self.current_file_path.rfind('.')
        if dot == -1:
            return f'{self.current_file_path}_cut.wav'
        return f'{self.current_file_path[:dot]}_cut{self.current_file_path[dot:]}'
