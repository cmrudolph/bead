from .color import Color
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def find_color_by_name(all_colors, name):
    for c in all_colors:
        if c.name == name:
            return c


class Palette:
    def __init__(self, all_colors, name_whitelist=None):
        self._colors = []
        if name_whitelist is not None and len(name_whitelist) > 0:
            # A filter was specified. Reduce the palette to only a subset of
            # all available colors
            for name in name_whitelist:
                match = find_color_by_name(all_colors, name)
                if match is None:
                    raise ValueError(f'Unknown color -- Name:{name}')
                self._colors.append(match)
        else:
            # No filtering - palette includes all available colors
            self._colors = all_colors[:]

        self._by_code_lookup = dict()
        self._by_hex_internal_lookup = dict()
        self._by_lab_lookup = dict()
        self._closest_cache = dict()

        for c in self._colors:
            self._by_code_lookup[c.code] = c
            self._by_hex_internal_lookup[c.hex_internal] = c

            # Compute and store each CIELab color because we will need these
            # for doing color comparisons later
            rgb = sRGBColor.new_from_rgb_hex(c.hex_internal)
            lab = convert_color(rgb, LabColor)
            self._by_lab_lookup[lab] = c

    @staticmethod
    def create_from_file(fp, name_whitelist=None):
        txt = fp.read()
        return Palette.create_from_txt(txt, name_whitelist)

    @staticmethod
    def create_from_txt(raw_txt, name_whitelist=None):
        colors = []
        lines = raw_txt.splitlines()[1:]
        for line in lines:
            splits = [x.strip() for x in line.split('|')]
            if len(splits) == 6:
                id = splits[0]
                code = splits[1]
                name = splits[2]
                internal = splits[3]

                # Optional component -- fall back to internal value
                view = splits[4].strip()
                view = internal if len(view) == 0 else view

                # Optional component -- fall back to internal value
                edge = splits[5].strip()
                edge = internal if len(edge) == 0 else edge

                colors.append(Color(id, code, name, internal, view, edge))
        return Palette(colors, name_whitelist)

    @property
    def colors(self):
        return self._colors

    def color_from_code(self, code):
        return self._by_code_lookup.get(code, None)

    def closest_color(self, r, g, b, a=255):
        if a == 0:
            # Transparent
            return None

        rgb = (r, g, b)
        cached = self._closest_cache.get(rgb, None)
        if cached is not None:
            # Already know the answer for this RGB value
            return cached
        else:
            # Compute cold and cache result
            rgb_color = sRGBColor(r, g, b, is_upscaled=True)
            lab = convert_color(rgb_color, LabColor)

            best_lab = None
            best_diff = 101
            for palette_lab in self._by_lab_lookup:
                diff = delta_e_cie2000(lab, palette_lab)
                if diff < best_diff:
                    best_diff = diff
                    best_lab = palette_lab

            color = self._by_lab_lookup[best_lab]
            self._closest_cache[rgb] = color

            return color
