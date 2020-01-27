import json


class BeadColor:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class BeadPalette:
    def __init__(self, colors):
        self._colors = colors

    @staticmethod
    def from_json(raw_json):
        d = json.loads(raw_json)

        colors = []
        for c in d["colors"]:
            name = c["name"]
            value = c["value"]
            colors.append(BeadColor(name, value))

        return BeadPalette(colors)

    @property
    def colors(self):
        return self._colors

    def has_color(self, value):
        return value in [c.value for c in self._colors]
