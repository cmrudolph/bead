from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPixmap
from canvas import BeadCanvas


class BeadPixmap(QPixmap):
    def __init__(self, layout, cell_size):
        self._cell_size = cell_size
        self._layout = layout
        self._bead_canvas = BeadCanvas(layout, cell_size)

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
            painter.drawRect(r[0], r[1], r[2], r[3])
        painter.end()

    def _render_beads(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1))

        for c in self._bead_canvas.circles:
            painter.setPen(QPen(QColor(c[3])))
            brush = QBrush()
            brush.setColor(QColor(c[4]))
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawEllipse(c[0], c[1], c[2], c[2])
        painter.end()
