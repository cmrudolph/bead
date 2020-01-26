import json


class BeadPalette:
    def __init__(self, colors):
        self._colors = colors

    @staticmethod
    def from_json(raw_json):
        d = json.loads(raw_json)

        colors = []
        for c in d["colors"]:
            hex_code = c["code"]
            colors.append(hex_code)

        return BeadPalette(colors)

    @property
    def colors(self):
        return self._colors

    def has_color(self, hex_color):
        return hex_color in self._colors
