NONE_CODE = '---'


class BeadLayout:
    def __init__(self, file, width, height, values):
        self._file = file
        self._width = width
        self._height = height
        self._values = values

    @staticmethod
    def create_new(file, width, height):
        values = [None] * (width * height)
        values = []
        for h in range(height):
            row_values = [None] * width
            values.append(row_values)
        layout = BeadLayout(file, width, height, values)
        layout._update_backing_file()

        return layout

    @staticmethod
    def load_from_file(fp):
        lines = [line.strip() for line in fp.readlines()]
        dims = [int(x) for x in lines[0].split('|')]
        width = dims[0]
        height = dims[1]
        values = []
        for h in range(1, height + 1):
            row_values = []
            for v in lines[h].split('|'):
                row_values.append(None if v == NONE_CODE else v)
            values.append(row_values)

        return BeadLayout(fp, width, height, values)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def values(self):
        return self._values

    def set_value(self, x, y, id):
        self._values[y][x] = id
        self._update_backing_file()

    def get_value(self, x, y):
        return self._values[y][x]

    def clear_value(self, x, y):
        self._values[y][x] = None
        self._update_backing_file()

    def _update_backing_file(self):
        self._file.seek(0)
        self._file.write('\n'.join(self._to_txt_lines()))
        self._file.truncate()

    def _to_txt_lines(self):
        lines = []
        lines.append(f'{self._width}|{self._height}')
        for row in self._values:
            s = '|'.join([NONE_CODE if x is None else x for x in row])
            lines.append(s)

        return lines
