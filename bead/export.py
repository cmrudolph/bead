import os
from .canvas import Canvas
from .layout import Layout
from .palette import Palette
from PIL import Image, ImageDraw, ImageColor


CELL_SIZE = 30


def export_layout(project):
    print(f'Exporting project -- Name:{project.name}')
    with open(project.layout_path, 'r') as layout_f:
        layout = Layout.load_from_file(layout_f)
        print(f'Dimensions -- W:{layout.width}; H:{layout.height}')

        # Make sure the project properties and the layout agree on the
        # dimensions of this pattern. Sanity check to make sure we don't have
        # a configuration or file mistake in the project.
        pw = project.properties.width
        if layout.width != pw:
            raise ValueError(f'Width error -- L:{layout.width} != P:{pw}')
        ph = project.properties.height
        if layout.height != ph:
            raise ValueError(f'Height error -- L:{layout.height} != P:{ph}')

        canvas = Canvas(layout, project.palette, CELL_SIZE)

        # Create a new, empty image of the proper dimensions. The image
        # dimensions are not the 'raw' dimensions of the layout. They must
        # be scaled by a constant number of pixels (pixels per bead).
        img = Image.new('RGB', (canvas.width, canvas.height), 'white')
        draw = ImageDraw.Draw(img)

        # Now draw the necessary shapes. The grid serves as a guideline to keep
        # one's position straight while the beads provide color info.
        _render_grid(draw, canvas)
        _render_beads(draw, canvas)

        print(f'Writing -- Path:{project.final_path}')
        img.save(project.final_path, 'PNG')


def _render_grid(draw, canvas):
    for r in canvas.rectangles:
        draw.rectangle((r.topleft, r.bottomright), outline='black')


def _render_beads(draw, canvas):
    for c in canvas.circles:
        coords = (c.topleft, c.bottomright)
        draw.ellipse(coords, fill=c.fill_color, outline=c.edge_color, width=2)
