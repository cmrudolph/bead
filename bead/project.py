from .palette import Palette
from .properties import Properties
from pathlib import Path
import os

PROPS_FILE = 'properties.json'
ORIG_FILE = 'original.png'
LAYOUT_FILE = 'layout.txt'


class Project:
    def __init__(self, project_dir):
        if project_dir is None or not os.path.exists(project_dir):
            raise ValueError(f'Project dir {project_dir} must exist')
        self._project_dir = project_dir

        # If project is at c:/Projects/Foo, name will be 'Foo'
        self._name = os.path.basename(os.path.normpath(project_dir))

        # A properties file is a requirement of instantiating a project
        # instance.
        self._properties_path = os.path.join(project_dir, PROPS_FILE)
        if not os.path.exists(self._properties_path):
            raise ValueError(f'File {self._properties_path} must exist')
        with open(self._properties_path, 'r') as f:
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
    def project_dir(self):
        return self._project_dir

    @property
    def properties_path(self):
        return self._properties_path

    @property
    def orig_path(self):
        return os.path.join(self._project_dir, ORIG_FILE)

    @property
    def gridified_path(self):
        return os.path.join(self._project_dir, 'gridified.png')

    @property
    def partitioned_path(self):
        return os.path.join(self._project_dir, 'partitioned.png')

    @property
    def quantized_path(self):
        return os.path.join(self._project_dir, 'quantized.png')

    @property
    def layout_path(self):
        return os.path.join(self._project_dir, LAYOUT_FILE)

    def get_transient_files(self):
        safe = [PROPS_FILE, ORIG_FILE, LAYOUT_FILE]
        files = os.listdir(self._project_dir)
        for f in files:
            if f not in safe:
                yield os.path.join(self._project_dir, f)

    @property
    def final_path(self):
        w = self._properties.width
        h = self._properties.height
        filename = f'{self._name}_{w}_{h}.png'
        return os.path.join(self._project_dir, filename)
