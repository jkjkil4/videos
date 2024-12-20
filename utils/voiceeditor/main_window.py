import subprocess as sp

import numpy as np
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLineEdit,
                               QPlainTextEdit, QPushButton, QVBoxLayout,
                               QWidget)
from timeline import SAMPLE_RATE, Timeline


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setup_ui()

        self.convert_timer = QTimer(self)
        self.convert_timer.setSingleShot(True)

        self.number.editingFinished.connect(self.on_number_editing_finished)
        self.editor.textChanged.connect(lambda: self.convert_timer.start(1000))
        self.convert_timer.timeout.connect(self.on_convert_timer_timeout)
        self.btn_open.clicked.connect(self.on_btn_open_clicked)
        self.btn_export.clicked.connect(self.on_btn_export_clicked)

        self.setWindowTitle('Voice Editor')
        self.resize(1000, 600)
        self.editor.setFocus()

    def setup_ui(self) -> None:
        self.number = QLineEdit()
        self.number.setText('1')
        self.editor = QPlainTextEdit()

        self.editor_layout = QVBoxLayout()
        self.editor_layout.addWidget(self.number)
        self.editor_layout.addWidget(self.editor)

        self.code_view = QPlainTextEdit()
        self.code_view.setReadOnly(True)

        self.top_layout = QHBoxLayout()
        self.top_layout.addLayout(self.editor_layout)
        self.top_layout.addWidget(self.code_view)

        self.timeline = Timeline()
        self.timeline.setMinimumHeight(100)

        self.btn_open = QPushButton('打开')
        self.btn_export = QPushButton('导出')

        self.btn_layout = QVBoxLayout()
        self.btn_layout.addWidget(self.btn_open)
        self.btn_layout.addWidget(self.btn_export)
        self.btn_layout.addStretch()

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.timeline, 1)
        self.bottom_layout.addLayout(self.btn_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout, 1)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

    def on_number_editing_finished(self) -> None:
        self.on_convert_timer_timeout()
        self.timeline.set_start_number(int(self.number.text()))

    def on_convert_timer_timeout(self) -> None:
        try:
            number = int(self.number.text())
        except ValueError:
            self.number.blockSignals(True)
            self.number.setText('1')
            self.number.blockSignals(False)
            number = 1

        results = []

        for line in self.editor.toPlainText().split('\n'):
            line = line.strip()
            if not line:
                continue
            results.append(f"t = self.aas('{number}'.mp3, {repr(line)})")
            number += 1

        result = '\nself.forward_to(t.end)\n'.join(results)
        self.code_view.setPlainText(result)

    def on_btn_open_clicked(self) -> None:
        file_path = QFileDialog.getOpenFileName(self, '打开音频')
        file_path = file_path[0]
        if not file_path:
            return

        command = [
            'ffmpeg',
            '-vn',
            '-i', file_path,
            '-f', 's16le',
            '-acodec', 'pcm_s16le',
            '-ar', str(SAMPLE_RATE),     # framerate & samplerate
            '-ac', '2',
            '-loglevel', 'error',
            '-',    # output to a pipe
        ]

        with sp.Popen(command, stdout=sp.PIPE) as reading_process:
            data = np.frombuffer(reading_process.stdout.read(), dtype=np.int16).reshape((-1, 2))

        self.timeline.set_samples(data)

    def on_btn_export_clicked(self) -> None:
        self.timeline.export()
