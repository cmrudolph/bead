import json


KEY_WIDTH = 'width'
KEY_HEIGHT = 'height'
KEY_QUANT = 'quantize_colors'
KEY_COLORS = 'colors'


class Properties:
    def __init__(self, width, height, quantize_colors, colors):
        self._width = width
        self._height = height
        self._quantize_colors = quantize_colors
        self._colors = () if colors is None else tuple(colors)

    @staticmethod
    def create(width, height, quant=0, colors=None):
        return Properties(width, height, quant, colors)

    @staticmethod
    def from_json(json_txt):
        d = json.loads(json_txt)
        width = int(d[KEY_WIDTH])
        height = int(d[KEY_HEIGHT])
        quantize_colors = int(d.get(KEY_QUANT, 0))
        colors = d.get(KEY_COLORS, [])

        return Properties(width, height, quantize_colors, colors)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def quantize_colors(self):
        return self._quantize_colors

    @property
    def colors(self):
        return self._colors

    def to_json(self):
        d = {
            KEY_WIDTH: self._width,
            KEY_HEIGHT: self._height,
            KEY_QUANT: self._quantize_colors,
            KEY_COLORS: self._colors
        }

        return json.dumps(d, indent=2)
