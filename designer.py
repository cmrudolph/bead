import fire
import os
import sys
from bead import Canvas, Layout, Palette
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication


CELL_SIZE = 25
PALETTE_BTN_SIZE = 20


class BeadPixmap(QPixmap):
    def __init__(self, layout, palette, cell_size):
        self._cell_size = cell_size
        self._layout = layout
        self._bead_canvas = Canvas(layout, palette, cell_size)

        pixel_width = layout.width * cell_size
        pixel_height = layout.height * cell_size
        super().__init__(pixel_width, pixel_height)

        self.fill(Qt.white)
        self._render_grid()
        self._render_beads()

    def _render_grid(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1))

        for r in self._bead_canvas.rectangles:
            x = r.topleft[0]
            y = r.topleft[1]
            painter.drawRect(x, y, r.width, r.height)
        painter.end()

    def _render_beads(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1))

        for c in self._bead_canvas.circles:
            painter.setPen(QPen(QColor(c.edge_color)))
            brush = QBrush()
            brush.setColor(QColor(c.fill_color))
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            x = c.topleft[0]
            y = c.topleft[1]
            painter.drawEllipse(x, y, c.diameter, c.diameter)
        painter.end()


class Canvas(QtWidgets.QLabel):
    def __init__(self, layout, palette):
        super().__init__()

        self._palette = palette
        self._bead_canvas = Canvas(layout, palette, CELL_SIZE)

        canvas_width = layout.width * CELL_SIZE
        canvas_height = layout.height * CELL_SIZE

        self.setMaximumWidth(canvas_width)
        self.setMaximumHeight(canvas_height)
        self._render_from_layout()

    def set_color(self, color):
        self._color = color

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._bead_canvas.try_set(e.x(), e.y(), self._color.code)
        else:
            self._bead_canvas.try_clear(e.x(), e.y())

        self._render_from_layout()

    def _render_from_layout(self):
        pixmap = BeadPixmap(self._bead_canvas.layout, self._palette, CELL_SIZE)
        self.setPixmap(pixmap)
        self.update()


class QPaletteButton(QtWidgets.QPushButton):
    def __init__(self, color, name):
        super().__init__()
        self.setFixedSize(QtCore.QSize(PALETTE_BTN_SIZE, PALETTE_BTN_SIZE))
        self.color = color
        self.setToolTip(f'{name} ({color})')
        self.setStyleSheet("background-color: %s;" % color)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, palette, layout):
        super().__init__()

        self.canvas = Canvas(layout, palette)

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
            b = QPaletteButton(c.hex_value, c.name)
            b.pressed.connect(lambda c=c: self.canvas.set_color(c))
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
            layout = Layout.create_new(f, width, height)
            self._launch_app(palette, layout)

    def load(self, palette_file, layout_file):
        palette = self._process_palette_file(palette_file)
        with open(layout_file, 'r+') as f:
            layout = Layout.load_from_file(f)
            self._launch_app(palette, layout)

    def _process_palette_file(self, palette_file):
        with open(palette_file, 'r') as f:
            p = Palette.load_from_file(f)
        return p

    def _launch_app(self, palette, layout):
        app = QApplication(sys.argv)
        window = MainWindow(palette, layout)
        window.show()
        app.exec_()


if __name__ == "__main__":
    fire.Fire(Cli)
