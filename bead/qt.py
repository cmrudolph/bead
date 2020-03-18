from .canvas import BeadCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPixmap


class BeadPixmap(QPixmap):
    def __init__(self, layout, palette, cell_size):
        self._cell_size = cell_size
        self._layout = layout
        self._bead_canvas = BeadCanvas(layout, palette, cell_size)

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
