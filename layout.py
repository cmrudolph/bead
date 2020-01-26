import json


class BeadLayout:
    def __init__(self, file, width, height, values):
        self._file = file
        self._width = width
        self._height = height
        self._values = values

    @staticmethod
    def create_new(file, width, height):
        values = [None] * (width * height)
        layout = BeadLayout(file, width, height, values)
        layout._update_backing_file()

        return layout

    @staticmethod
    def create_from_file(file):
        content = file.read()
        d = json.loads(content)
        width = d['width']
        height = d['height']
        values = d['values']

        return BeadLayout(file, width, height, values)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def values(self):
        return self._values

    def set_value(self, x, y, hex_color):
        _idx = self._compute_idx(x, y)
        self._values[_idx] = hex_color
        self._update_backing_file()

    def get_value(self, x, y):
        _idx = self._compute_idx(x, y)
        return self._values[_idx]

    def clear_value(self, x, y):
        _idx = self._compute_idx(x, y)
        self._values[_idx] = None
        self._update_backing_file()

    def replace_values(self, hex_color_orig, hex_color_new):
        for i, v in enumerate(self._values):
            if v == hex_color_orig:
                self._values[i] = hex_color_new
        self._update_backing_file()

    def _update_backing_file(self):
        self._file.seek(0)
        self._file.write(self._to_json())
        self._file.truncate()

    def _to_json(self):
        d = dict()
        d['width'] = self._width
        d['height'] = self._height
        d['values'] = self._values

        return json.dumps(d)

    def _compute_idx(self, x, y):
        return (y * self._width) + x
