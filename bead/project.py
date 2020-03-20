from .palette import Palette
from .properties import Properties
from pathlib import Path
import os


class Project:
    def __init__(self, root_dir, name):
        if root_dir is None or not os.path.exists(root_dir):
            raise ValueError(f'Root dir {root_dir} must exist')
        self._root_dir = root_dir
        self._name = name
        self._project_folder = os.path.join(root_dir, name)

        props_path = os.path.join(self._project_folder, 'properties.json')
        with open(props_path, 'r') as f:
            self._properties = Properties.load_from_file(f)

        # The master palette lives with the source. It is effectively a baked
        # in detail of the application. Projects can override the set of
        # available colors via filtering if they desire.
        palette_path = Path(__file__).parent.parent.joinpath('palette.txt')
        with open(palette_path, 'r') as palette_f:
            whitelist = None
            colors_path = os.path.join(self._project_folder, 'colors.txt')
            if os.path.exists(colors_path):
                with open(colors_path, 'r') as colors_f:
                    whitelist = [x.strip() for x in colors_f.readlines()]

            self._palette = Palette.create_from_file(palette_f, whitelist)

    @property
    def name(self):
        return self._name

    @property
    def palette(self):
        return self._palette

    @property
    def properties(self):
        return self._properties

    @property
    def orig_path(self):
        return os.path.join(self._project_folder, 'original.png')

    @property
    def quantized_path(self):
        return os.path.join(self._project_folder, 'quantized.png')

    @property
    def partitioned_path(self):
        return os.path.join(self._project_folder, 'partitioned.png')

    @property
    def layout_path(self):
        return os.path.join(self._project_folder, 'layout.txt')

    @property
    def final_path(self):
        return os.path.join(self._project_folder, 'final.png')
