import os
from .layout import BeadLayout
from .palette import BeadPalette


def generate_layout(palette_path, image_path, layout_path, width, height):
    if os.path.exists(layout_path):
        os.remove(layout_path)

    with open(layout_path, 'w') as layout_f:
        with open(palette_path, 'r') as palette_f:
            layout = BeadLayout.create_new(layout_f, width, height)
            palette = BeadPalette.load_from_file(palette_f)
