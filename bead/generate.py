import os
import multiprocessing as mp
from .layout import Layout
from .palette import Palette
from collections import Counter
from PIL import Image


def generate_layout(palette_path, image_path, layout_path, width, height):
    if os.path.exists(layout_path):
        os.remove(layout_path)

    with open(layout_path, 'w') as layout_f:
        with open(palette_path, 'r') as palette_f:
            layout = Layout.create_new(layout_f, width, height)
            palette = Palette.load_from_file(palette_f)

            img = Image.open(image_path)

            pixels = []
            for y in range(img.height):
                row_pixels = []
                for x in range(img.width):
                    row_pixels.append(img.getpixel((x, y)))
                pixels.append(row_pixels)

            cell_width = img.width // width
            cell_width_rem = img.width % width
            cell_height = img.height // height
            cell_height_rem = img.height % height

            best_color_cache = dict()
            for h in range(height):
                for w in range(width):
                    cell_pixels = []
                    final_cell_width = cell_width
                    final_cell_height = cell_height
                    if w == width - 1:
                        final_cell_width += cell_width_rem
                    if h == height - 1:
                        final_cell_height += cell_height_rem

                    h_offset = h * cell_height
                    w_offset = w * cell_width

                    for y in range(h_offset, final_cell_height + h_offset):
                        for x in range(w_offset, final_cell_width + w_offset):
                            cell_pixels.append(pixels[y][x])

                    color_count = Counter()
                    for cp in cell_pixels:
                        rgb = (cp[0], cp[1], cp[2])
                        cached = best_color_cache.get(rgb, None)
                        if img.mode == 'RGBA' and cp[3] == 0:
                            color_count[None] += 1
                        elif cached is not None:
                            color_count[cached] += 1
                        else:
                            cell_color = palette.closest_color(*rgb)
                            best_color_cache[rgb] = cell_color.code
                            color_count[cell_color.code] += 1

                    best_color = color_count.most_common(1)[0][0]
                    layout.set_value(w, h, best_color)
