import fire
import pathlib
import os
import sys
from canvas import BeadCanvas
from layout import BeadLayout
from palette import BeadPalette
from qt_helper import BeadPixmap
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

CELL_SIZE = 25
PALETTE_BTN_SIZE = 20


class Canvas(QtWidgets.QLabel):
    def __init__(self, layout):
        super().__init__()

        self._bead_canvas = BeadCanvas(layout, CELL_SIZE)
        self._pen_color = QtGui.QColor('#000000')

        canvas_width = layout.width * CELL_SIZE
        canvas_height = layout.height * CELL_SIZE

        self.setMaximumWidth(canvas_width)
        self.setMaximumHeight(canvas_height)
        self._render_from_layout()

    def set_pen_color(self, c):
        self._pen_color = QtGui.QColor(c)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._bead_canvas.try_set(e.x(), e.y(), self._pen_color.name())
        else:
            self._bead_canvas.try_clear(e.x(), e.y())

        self._render_from_layout()

    def _render_from_layout(self):
        pixmap = BeadPixmap(self._bead_canvas.layout, CELL_SIZE)
        self.setPixmap(pixmap)
        self.update()


class QPaletteButton(QtWidgets.QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(PALETTE_BTN_SIZE, PALETTE_BTN_SIZE))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, palette, layout):
        super().__init__()

        self.canvas = Canvas(layout)

        widget = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        widget.setLayout(hbox)

        palette_widget = QtWidgets.QGridLayout()
        self._add_palette_buttons(palette_widget, palette)
        hbox.addLayout(palette_widget)

        hbox.addWidget(self.canvas)

        self.setCentralWidget(widget)

    def _add_palette_buttons(self, layout, palette):
        row = 0
        col = -1
        for i, c in enumerate(palette.colors):
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            if col == 1:
                row += 1
                col = 0
            else:
                col += 1
            layout.addWidget(b, row, col)


class Cli():
    def new(self, palette_file, layout_file, width, height, force=False):
        if os.path.exists(layout_file):
            if force:
                os.remove(layout_file)
            else:
                raise Exception('File already exists!')

        palette = self._process_palette_file(palette_file)
        with open(layout_file, 'w+') as f:
            layout = BeadLayout.create_new(f, width, height)
            self._launch_app(palette, layout)

    def load(self, palette_file, layout_file):
        palette = self._process_palette_file(palette_file)
        with open(layout_file, 'r+') as f:
            layout = BeadLayout.create_from_file(f)
            self._launch_app(palette, layout)

    def _process_palette_file(self, palette_file):
        raw_json = pathlib.Path(palette_file).read_text()
        p = BeadPalette.from_json(raw_json)
        return p

    def _launch_app(self, palette, layout):
        app = QApplication(sys.argv)
        window = MainWindow(palette, layout)
        window.show()
        app.exec_()


if __name__ == "__main__":
    fire.Fire(Cli)