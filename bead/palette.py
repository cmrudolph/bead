from .color import BeadColor
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


class BeadPalette:
    def __init__(self, colors):
        self._colors = colors
        self._by_code_lookup = dict()
        self._by_hex_value_lookup = dict()
        self._by_lab_lookup = dict()

        for c in colors:
            print(f'Palette Color: {c}')
            self._by_code_lookup[c.code] = c
            self._by_hex_value_lookup[c.hex_value] = c

            # Compute and store each CIELab color because we will need these
            # for doing color comparisons later
            rgb = sRGBColor.new_from_rgb_hex(c.hex_value)
            lab = convert_color(rgb, LabColor)
            self._by_lab_lookup[lab] = c

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

    def closest_color(self, r, g, b):
        rgb = sRGBColor(r, g, b, is_upscaled=True)
        lab = convert_color(rgb, LabColor)

        best = None
        best_diff = 101
        for palette_lab in self._by_lab_lookup:
            diff = delta_e_cie2000(lab, palette_lab)
            if diff < best_diff:
                best_diff = diff
                best = palette_lab

        return self._by_lab_lookup[best]
