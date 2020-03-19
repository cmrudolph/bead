import json


class BeadProperties:
    def __init__(self, d):
        self._width = int(d['width'])
        self._height = int(d['height'])
        self._quantize_colors = int(d['quantize_colors'])
        self._colors = d['colors']

    @staticmethod
    def load_from_file(fp):
        json_txt = fp.read()
        return BeadProperties.load_from_json(json_txt)

    @staticmethod
    def load_from_json(json_txt):
        json_dict = json.loads(json_txt)
        return BeadProperties.load_from_dict(json_dict)

    @staticmethod
    def load_from_dict(d):
        return BeadProperties(d)

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
        return self._colors[:]
