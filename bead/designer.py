import os
import sys
from .canvas import Canvas
from .layout import Layout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QColor, QPainter, QPen, QBrush, QPixmap)
from PyQt5.QtWidgets import QApplication


CELL_SIZE = 25
PALETTE_BTN_SIZE = 20


def design_layout(project):
    with open(project.layout_path, 'r+') as f:
        layout = Layout.load_from_file(f)
        app = QApplication(sys.argv)
        window = MainWindow(project, layout)
        window.show()
        app.exec_()


class BeadPixmap(QPixmap):
    def __init__(self, project, layout, cell_size):
        self._cell_size = cell_size
        self._layout = layout
        self._bead_canvas = Canvas(layout, project.palette, cell_size)

        pixel_width = layout.width * cell_size
        pixel_height = layout.height * cell_size

        if os.path.exists(project.partitioned_path):
            # If a partitioned file exists, assume we want the designer to
            # use said image as the background. This makes bead placement
            # easier since an image will be visible.
            super().__init__(project.partitioned_path)
        else:
            # Default = just render a white background
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


class DesignerCanvas(QtWidgets.QLabel):
    def __init__(self, project, layout):
        super().__init__()

        self._project = project
        self._palette = project.palette
        self._layout = layout
        self._bead_canvas = Canvas(layout, project.palette, CELL_SIZE)

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
        pixmap = BeadPixmap(self._project, self._layout, CELL_SIZE)
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
    def __init__(self, project, layout):
        super().__init__()

        self.canvas = DesignerCanvas(project, layout)

        widget = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        widget.setLayout(hbox)

        palette_widget = QtWidgets.QGridLayout()
        self._add_palette_buttons(palette_widget, project.palette)
        hbox.addLayout(palette_widget)

        hbox.addWidget(self.canvas)

        self.setCentralWidget(widget)

    def _add_palette_buttons(self, layout, palette):
        row = 0
        col = -1
        for i, c in enumerate(palette.colors):
            b = QPaletteButton(c.hex_view, c.name)
            b.pressed.connect(lambda c=c: self.canvas.set_color(c))
            if col == 1:
                row += 1
                col = 0
            else:
                col += 1
            layout.addWidget(b, row, col)
