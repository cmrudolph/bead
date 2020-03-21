from .palette import Palette
from .properties import Properties
from pathlib import Path
import os


class Project:
    def __init__(self, project_dir):
        if project_dir is None or not os.path.exists(project_dir):
            raise ValueError(f'Project dir {project_dir} must exist')
        self._project_dir = project_dir

        # If project is at c:/Projects/Foo, name will be 'Foo'
        self._name = os.path.basename(os.path.normpath(project_dir))

        # A properties file is a requirement of instantiating a project
        # instance.
        props_path = os.path.join(project_dir, 'properties.json')
        if not os.path.exists(props_path):
            raise ValueError(f'File {props_path} must exist')
        with open(props_path, 'r') as f:
            props_txt = f.read()
            self._properties = Properties.from_json(props_txt)

        # The master palette lives with the source. It is effectively a baked
        # in detail of the application. Projects can override the set of
        # available colors via filtering if they desire.
        palette_path = Path(__file__).parent.parent.joinpath('palette.txt')
        with open(palette_path, 'r') as f:
            whitelist = self._properties.colors
            self._palette = Palette.create_from_file(f, whitelist)

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
        return os.path.join(self._project_dir, 'original.png')

    @property
    def cropped_path(self):
        return os.path.join(self._project_dir, 'cropped.png')

    @property
    def quantized_path(self):
        return os.path.join(self._project_dir, 'quantized.png')

    @property
    def partitioned_path(self):
        return os.path.join(self._project_dir, 'partitioned.png')

    @property
    def layout_path(self):
        return os.path.join(self._project_dir, 'layout.txt')

    @property
    def final_path(self):
        return os.path.join(self._project_dir, 'final.png')
