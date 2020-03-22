import math
import numpy as np
import os
from .canvas import Canvas
from .layout import Layout
from .palette import Palette
from PIL import Image, ImageDraw, ImageColor


def partition_image(project):
    print(f'Partitioning image -- Name:{project.name}')

    if not os.path.exists(project.orig_path):
        raise ValueError(f'File missing -- Path:{project.orig_path}')

    img = Image.open(project.orig_path)

    # First crop to remove all transparent pixels from the edges. This makes
    # sure the actual image is framed as tightly as possible.
    cropped_img = crop_image(img)

    # Next, scale the image based on the number of beads we want in each
    # direction. This produces an image with nice, round numbers to simplify
    # future processing
    scaled_img = scale_image(cropped_img, project)

    # Split the image into rectangles by inserting transparent rows and columns
    # at the right places in the matrix. Each rectangle corresponds to a single
    # bead
    trans = (0, 0, 0, 0)
    grid_transparent_img = gridify_image(scaled_img, project, trans, trans)

    # Also perform the splitting exercise, but with colored row and column
    # lines instead of transparent ones. This helps make it obvious where the
    # grid overlay falls on the image
    red = (255, 0, 0, 255)
    blue = (0, 0, 255, 255)
    grid_colored_img = gridify_image(scaled_img, project, red, blue)

    transparent_pixel = (0, 0, 0, 0)

    print(f'Writing -- Path:{project.partitioned_path}')
    grid_transparent_img.save(project.partitioned_path, 'PNG')

    print(f'Writing -- Path:{project.gridified_path}')
    grid_colored_img.save(project.gridified_path, 'PNG')


def crop_image(img):
    print('Cropping image')

    non_transparent_rows = find_non_transparent_rows(img)
    non_transparent_cols = find_non_transparent_cols(img)

    (w, h) = img.size
    print(f'Before -- W:{w}; H:{h}')

    top = min(non_transparent_rows)
    bottom = max(non_transparent_rows)
    left = min(non_transparent_cols)
    right = max(non_transparent_cols)

    r_trimmed = w - right - 1
    b_trimmed = h - bottom - 1
    print(f'Trimmed -- L:{left}; R:{r_trimmed}; T:{top}; B:{b_trimmed}')

    cropped_img = img.crop((left, top, right + 1, bottom + 1))

    cropped_size = cropped_img.size
    print(f'After -- W:{cropped_size[0]}; H:{cropped_size[1]}')

    return cropped_img


def scale_image(img, project):
    print('Scaling image')

    (w, h) = img.size
    print(f'Before -- W:{w}; H:{h}')

    proj_w = project.properties.width
    proj_h = project.properties.height
    scaled_w = math.ceil(w / proj_w) * proj_w
    scaled_h = math.ceil(h / proj_h) * proj_h
    scaled_img = img.resize((scaled_w, scaled_h))

    scaled_size = scaled_img.size
    print(f'After -- W:{scaled_size[0]}; H:{scaled_size[1]}')

    return scaled_img


def gridify_image(img, project, row_pixel, col_pixel):
    (w, h) = img.size
    a = np.array(img)

    proj_w = project.properties.width
    proj_h = project.properties.height
    step_w = w // proj_w
    step_h = h // proj_h

    # Insert columns of consistent pixels at all the relevant steps along the
    # way (step = dividing line between neighboring beads)
    for x in range(w-step_w, 0, -1 * step_w):
        a = np.insert(a, x, col_pixel, 1)

    # Insert rows of consistent pixels at all the relevant steps along the
    # way (step = dividing line between neighboring beads)
    for y in range(h-step_h, 0, -1 * step_h):
        a = np.insert(a, y, row_pixel, 0)

    new_h = a.shape[0]
    new_w = a.shape[1]
    gridified_img = Image.frombytes('RGBA', (new_w, new_h), a)

    return gridified_img


def find_non_transparent_rows(img):
    (cols, rows) = img.size
    results = []

    for row in range(rows):
        all_transparent = True
        for col in range(cols):
            pixel = img.getpixel((col, row))
            if not is_transparent_pixel(pixel):
                all_transparent = False
                break
        if not all_transparent:
            results.append(row)

    return results


def find_non_transparent_cols(img):
    (cols, rows) = img.size
    results = []

    for col in range(cols):
        all_transparent = True
        for row in range(rows):
            pixel = img.getpixel((col, row))
            if not is_transparent_pixel(pixel):
                all_transparent = False
                break
        if not all_transparent:
            results.append(col)

    return results


def is_transparent_pixel(pixel):
    return len(pixel) >= 4 and pixel[3] == 0
