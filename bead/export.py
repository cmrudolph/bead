import os
from .layout import BeadLayout
from .palette import BeadPalette
from .qt import BeadPixmap
from PyQt5.QtWidgets import QApplication


def export_layout(palette_path, layout_path, output_path, cell_size):
    if os.path.exists(output_path):
        os.remove(output_path)

    with open(layout_path, 'r') as layout_f:
        with open(palette_path, 'r') as palette_f:
            layout = BeadLayout.load_from_file(layout_f)
            palette = BeadPalette.load_from_file(palette_f)

            app = QApplication([])
            pixmap = BeadPixmap(layout, palette, cell_size)
            pixmap.save(output_path, 'PNG')
