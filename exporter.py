import fire
import os
import sys
from layout import BeadLayout
from PyQt5.QtWidgets import QApplication
from qt_helper import BeadPixmap


class Cli():
    def export(self, layout_file, image_file, cell_size, force=False):
        if os.path.exists(image_file):
            if force:
                os.remove(image_file)
            else:
                raise Exception('Image file already exists!')

        with open(layout_file, 'r+') as f:
            layout = BeadLayout.create_from_file(f)
            app = QApplication(sys.argv)
            pixmap = BeadPixmap(layout, cell_size)
            pixmap.save(image_file, 'PNG')


if __name__ == "__main__":
    fire.Fire(Cli)
