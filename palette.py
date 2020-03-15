import json


class BeadColor:
    def __init__(self, id, name, hex_value):
        self._id = id
        self._name = name
        self._hex_value = hex_value

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def hex_value(self):
        return self._hex_value


class BeadPalette:
    def __init__(self, colors):
        self._colors = colors

    @staticmethod
    def from_txt(raw_txt):
        colors = []
        lines = raw_txt.splitlines()
        for line in lines:
            splits = [x.strip() for x in line.split('|')]
            if len(splits) == 3:
                id = splits[0]
                name = splits[1]
                hex_value = splits[2]
                colors.append(BeadColor(id, name, hex_value))

        return BeadPalette(colors)

    @property
    def colors(self):
        return self._colors

    def id_from_hex_value(self, hex_value):
        for_compare = hex_value.lower()
        for c in self._colors:
            if c.hex_value == for_compare:
                return c.id

    def hex_value_from_id(self, id):
        for c in self._colors:
            if c.id == id:
                return c.hex_value
