import os
from .canvas import Canvas
from .layout import Layout
from .palette import Palette
from PIL import Image, ImageDraw, ImageColor


CELL_SIZE = 30


def is_transparent_pixel(pixel):
    return pixel[3] == 0


def crop_image(project):
    print(f'Cropping image -- Name:{project.name}')

    if not os.path.exists(project.orig_path):
        raise ValueError(f'File missing -- Path:{project.orig_path}')

    img = Image.open(project.orig_path)
    (cols, rows) = img.size
    start_row = 0
    start_col = 0
    end_row = rows-1
    end_col = cols-1

    non_transparent_rows = []
    non_transparent_cols = []

    for row in range(rows):
        all_transparent = True
        for col in range(cols):
            pixel = img.getpixel((col, row))
            if not is_transparent_pixel(pixel):
                all_transparent = False
                break
        if not all_transparent:
            non_transparent_rows.append(row)

    for col in range(cols):
        all_transparent = True
        for row in range(rows):
            pixel = img.getpixel((col, row))
            if not is_transparent_pixel(pixel):
                all_transparent = False
                break
        if not all_transparent:
            non_transparent_cols.append(col)

    start_row = min(non_transparent_rows)
    end_row = max(non_transparent_rows)
    start_col = min(non_transparent_cols)
    end_col = max(non_transparent_cols)

    print(f'Orig img -- W:{cols}; H:{rows}')

    cropped_img = img.crop((start_col, start_row, end_col + 1, end_row + 1))
    cropped_size = cropped_img.size
    print(f'Cropped img -- W:{cropped_size[0]}; H:{cropped_size[1]}')

    print(f'Writing -- Path:{project.cropped_path}')
    cropped_img.save(project.cropped_path, 'PNG')
