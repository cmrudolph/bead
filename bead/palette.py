from .color import BeadColor


class BeadPalette:
    def __init__(self, colors):
        self._colors = colors
        self._by_code_lookup = dict()
        self._by_hex_value_lookup = dict()

        for c in colors:
            print(f'Palette Color: {c}')
            self._by_code_lookup[c.code] = c
            self._by_hex_value_lookup[c.hex_value] = c

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
        return self._by_hex_value_lookup.get(hex_value.lower(), None)

    def color_from_code(self, code):
        return self._by_code_lookup.get(code, None)
