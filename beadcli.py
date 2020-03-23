import fire
import os
from bead import (Project, export_layout, generate_layout, quantize_image,
                  design_layout, partition_image)


class Cli():
    def __init__(self):
        self._root = os.getenv('BEADROOT')

    def design(self, project_name):
        project = Project(os.path.join(self._root, project_name))
        design_layout(project)

    def export(self, project_name):
        project = Project(os.path.join(self._root, project_name))
        export_layout(project)

    def generate(self, project_name, force=False):
        project = Project(os.path.join(self._root, project_name))
        generate_layout(project, force)

    def partition(self, project_name):
        project = Project(os.path.join(self._root, project_name))
        partition_image(project)

    def quantize(self, project_name):
        project = Project(os.path.join(self._root, project_name))
        quantize_image(project)


if __name__ == "__main__":
    fire.Fire(Cli)
