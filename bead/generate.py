import os
from .layout import Layout
from collections import Counter
from PIL import Image


def generate_layout(project, force=False):
    print(f'Generating layout -- Name:{project.name}; Force:{force}')

    if not os.path.exists(project.quantized_path):
        raise ValueError(f'File missing -- Path:{project.quantized_path}')

    if os.path.exists(project.layout_path) and not force:
        raise ValueError('Layout exists and force not specified')

    width = project.properties.width
    height = project.properties.height

    with open(project.layout_path, 'w') as layout_f:
        layout = Layout.create_new(layout_f, width, height)
        img = Image.open(project.quantized_path)

        cell_width = img.width // width
        cell_height = img.height // height

        h_offset = 0
        for h in range(height):
            w_offset = 0
            for w in range(width):
                color_count = Counter()

                for y in range(h_offset, h_offset + cell_height):
                    for x in range(w_offset, w_offset + cell_width):
                        pixel = img.getpixel((x, y))

                        # Palette handles this efficiently (caching of lookups
                        # that have already been asked for)
                        color = project.palette.closest_color(*pixel)
                        code = None
                        code = color.code if color is not None else None
                        color_count[code] += 1

                best_color = color_count.most_common(1)[0][0]
                layout.set_value(w, h, best_color)

                w_offset += cell_width + 1
            h_offset += cell_height + 1
