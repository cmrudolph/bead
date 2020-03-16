import json


class BeadColor:
    def __init__(self, id, code, name, hex_value):
        self._id = id
        self._code = code.upper()
        self._name = name
        self._hex_value = hex_value.lower()

    def __repr__(self):
        return (f"BeadColor('{self._id}', '{self.code}', '{self.name}', "
                f"'{self.hex_value}')")

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def hex_value(self):
        return self._hex_value

    def is_white(self):
        return self._code == 'WHT'


class BeadPalette:
    def __init__(self, colors):
        self._colors = colors
        self._code_to_hex = dict()
        self._hex_to_code = dict()

        for c in colors:
            print(f'Palette Color: {c}')
            self._code_to_hex[c.code] = c
            self._hex_to_code[c.hex_value] = c

    @staticmethod
    def load_from_file(fp):
        txt = fp.read()
        return BeadPalette.load_from_txt(txt)

    @staticmethod
    def load_from_txt(raw_txt):
        colors = []
        lines = raw_txt.splitlines()
        for line in lines:
            splits = [x.strip() for x in line.split('|')]
            if len(splits) == 4:
                id = splits[0]
                code = splits[1]
                name = splits[2]
                hex_value = splits[3]
                colors.append(BeadColor(id, code, name, hex_value))
        return BeadPalette(colors)

    @property
    def colors(self):
        return self._colors

    def color_from_hex_value(self, hex_value):
        return self._hex_to_code.get(hex_value.lower(), None)

    def color_from_code(self, code):
        return self._code_to_hex.get(code, None)
