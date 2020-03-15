import fire
import os
import pathlib
import sys
from layout import BeadLayout
from palette import BeadPalette
from PyQt5.QtWidgets import QApplication
from qt_helper import BeadPixmap


class Cli():
    def export(self, layout_file, palette_file, image_file, cell_size, force=False):
        if os.path.exists(image_file):
            if force:
                os.remove(image_file)
            else:
                raise Exception('Image file already exists!')

        with open(layout_file, 'r+') as f:
            layout = BeadLayout.create_from_file(f)
            palette = self._process_palette_file(palette_file)
            app = QApplication(sys.argv)
            pixmap = BeadPixmap(layout, palette, cell_size)
            pixmap.save(image_file, 'PNG')

    def _process_palette_file(self, palette_file):
            raw_txt = pathlib.Path(palette_file).read_text()
            p = BeadPalette.from_txt(raw_txt)
            return p

if __name__ == "__main__":
    fire.Fire(Cli)
