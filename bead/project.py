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

        palette_path = Path(__file__).parent.parent.joinpath('palette.txt')
        with open(palette_path, 'r') as f:
            self._palette = Palette.create_from_file(f)

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
