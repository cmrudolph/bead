import os
from .canvas import Canvas
from .layout import Layout
from .palette import Palette
from PIL import Image, ImageDraw, ImageColor


def export_layout(palette_path, layout_path, image_path, cell_size):
    if os.path.exists(image_path):
        os.remove(image_path)

    with open(layout_path, 'r') as layout_f:
        with open(palette_path, 'r') as palette_f:
            layout = Layout.load_from_file(layout_f)
            palette = Palette.load_from_file(palette_f)

            canvas = Canvas(layout, palette, cell_size)
            w = layout.width * cell_size
            h = layout.height * cell_size

            img = Image.new('RGB', (w, h), 'white')
            draw = ImageDraw.Draw(img)

            _render_grid(draw, canvas)
            _render_beads(draw, canvas)

            img.save(image_path, 'PNG')


def _render_grid(draw, canvas):
    for r in canvas.rectangles:
        draw.rectangle((r.topleft, r.bottomright), outline='black')


def _render_beads(draw, canvas):
    for c in canvas.circles:
        coords = (c.topleft, c.bottomright)
        draw.ellipse(coords, fill=c.fill_color, outline=c.edge_color, width=2)
