class Line():
    def __init__(self, point1, point2):
        self._point1 = point1
        self._point2 = point2

    @property
    def point1(self):
        return self._point1

    @property
    def point2(self):
        return self._point2


class Circle():
    def __init__(self, x, y, diameter, fill_color, edge_color):
        self._topleft = (x, y)
        self._bottomright = (x + diameter, y + diameter)
        self._diameter = diameter
        self._fill_color = fill_color
        self._edge_color = edge_color

    @property
    def topleft(self):
        return self._topleft

    @property
    def bottomright(self):
        return self._bottomright

    @property
    def diameter(self):
        return self._diameter

    @property
    def fill_color(self):
        return self._fill_color

    @property
    def edge_color(self):
        return self._edge_color


class Canvas():
    def __init__(self, layout, palette, cell_size):
        self._layout = layout
        self._palette = palette
        self._cell_size = cell_size
        self._pixel_width = layout.width * cell_size + (layout.width - 1)
        self._pixel_height = layout.height * cell_size + (layout.height - 1)
        self._derive_shapes()

    @property
    def layout(self):
        return self._layout

    @property
    def lines(self):
        return self._lines

    @property
    def circles(self):
        return self._circles

    @property
    def width(self):
        return self._pixel_width

    @property
    def height(self):
        return self._pixel_height

    def try_set(self, pixel_x, pixel_y, color_id):
        coords = self._calculate_layout_coordinates(pixel_x, pixel_y)
        if coords is None:
            return

        # If the cell has nothing in it, store the the current color
        # there. If something already lives there, avoid overwriting. This
        # makes it harder to make a mistake (must right click first).
        if self._layout.get_value(coords[0], coords[1]) is None:
            self._layout.set_value(coords[0], coords[1], color_id)
        self._derive_shapes()

    def try_clear(self, pixel_x, pixel_y):
        coords = self._calculate_layout_coordinates(pixel_x, pixel_y)
        if coords is None:
            return

        self._layout.clear_value(coords[0], coords[1])
        self._derive_shapes()

    def _calculate_layout_coordinates(self, pixel_x, pixel_y):
        # Clicked on an edge. Ambiguous, so take no action.
        if pixel_x > 0 and pixel_x % self._cell_size == 0:
            return None
        if pixel_y > 0 and pixel_y % self._cell_size == 0:
            return None

        # X and Y in the layout are in terms of cells (beads), not pixels
        layout_x = pixel_x // (self._cell_size + 1)
        layout_y = pixel_y // (self._cell_size + 1)

        return (layout_x, layout_y)

    def _derive_shapes(self):
        self._derive_lines()
        self._derive_circles()

    def _derive_lines(self):
        self._lines = []
        cell_size = self._cell_size

        # Insert columns of consistent pixels at all the relevant steps along
        # the way (step = dividing line between neighboring beads)
        pw = self._pixel_width
        for x in range(cell_size, pw - cell_size, cell_size + 1):
            point1 = (x, 0)
            point2 = (x, self.height)
            self._lines.append(Line(point1, point2))

        # Insert rows of consistent pixels at all the relevant steps along the
        # way (step = dividing line between neighboring beads)
        ph = self._pixel_height
        for y in range(cell_size, ph - cell_size, cell_size + 1):
            point1 = (0, y)
            point2 = (self.width, y)
            self._lines.append(Line(point1, point2))

    def _derive_circles(self):
        self._circles = []
        for i in range(self._layout.width):
            for j in range(self._layout.height):
                value = self._layout.get_value(i, j)
                color = self._palette.color_from_code(value)

                if color is None:
                    # EMPTY = draw pure white (no circle)
                    continue
                else:
                    # OTHER = draw colored circle
                    edge_color = color.hex_edge
                    fill_color = color.hex_view

                # Include an offset + some padding so the circles do not go
                # all the way to the grid edges (breathing room)
                x = (i * (self._cell_size + 1)) + 1
                y = (j * (self._cell_size + 1)) + 1
                diameter = self._cell_size - 3

                circle = Circle(x, y, diameter, fill_color, edge_color)
                self._circles.append(circle)
