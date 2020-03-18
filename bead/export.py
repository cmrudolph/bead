import os
from .canvas import BeadCanvas
from .layout import BeadLayout
from .palette import BeadPalette
from PIL import Image, ImageDraw, ImageColor


def export_layout(palette_path, layout_path, output_path, cell_size):
    if os.path.exists(output_path):
        os.remove(output_path)

    with open(layout_path, 'r') as layout_f:
        with open(palette_path, 'r') as palette_f:
            layout = BeadLayout.load_from_file(layout_f)
            palette = BeadPalette.load_from_file(palette_f)

            canvas = BeadCanvas(layout, palette, cell_size)
            w = layout.width * cell_size
            h = layout.height * cell_size

            img = Image.new('RGB', (w, h), 'white')
            draw = ImageDraw.Draw(img)

            _render_grid(draw, canvas)
            _render_beads(draw, canvas)

            img.save(output_path, 'PNG')


def _render_grid(draw, canvas):
    for r in canvas.rectangles:
        xy1 = (r[0], r[1])
        xy2 = (r[0] + r[2], r[1] + r[3])

        draw.rectangle((xy1, xy2), outline='black')


def _render_beads(draw, canvas):
    for c in canvas.circles:
        xy1 = (c[0], c[1])
        xy2 = (c[0] + c[2], c[1] + c[2])
        edge_color = ImageColor.getrgb(c[3])
        fill_color = ImageColor.getrgb(c[4])

        draw.ellipse((xy1, xy2), fill=fill_color, outline=edge_color, width=2)
