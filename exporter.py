import fire
import os
import sys
from lib import BeadLayout, BeadPalette, BeadPixmap
from PyQt5.QtWidgets import QApplication


class Cli():
    def export(self, layout_file, palette_file, image_file, cell_size, force=False):
        if os.path.exists(image_file):
            if force:
                os.remove(image_file)
            else:
                raise Exception('Image file already exists!')

        with open(layout_file, 'r+') as f:
            layout = BeadLayout.load_from_file(f)
            palette = self._process_palette_file(palette_file)
            app = QApplication(sys.argv)
            pixmap = BeadPixmap(layout, palette, cell_size)
            pixmap.save(image_file, 'PNG')

    def _process_palette_file(self, palette_file):
        with open(palette_file, 'r') as f:
            p = BeadPalette.load_from_file(f)
        return p

if __name__ == "__main__":
    fire.Fire(Cli)
