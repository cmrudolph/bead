import fire
import os
from bead import (Project, export_layout, generate_layout, quantize_image,
                  design_layout)


Root = None


class Cli():
    def design(self, project_name):
        project = Project(os.path.join(Root, project_name))
        design_layout(project)

    def export(self, project_name):
        project = Project(os.path.join(Root, project_name))
        export_layout(project)

    def generate(self, project_name, force=False):
        project = Project(os.path.join(Root, project_name))
        generate_layout(project, force)

    def quantize(self, project_name):
        project = Project(os.path.join(Root, project_name))
        quantize_image(project)


if __name__ == "__main__":
    Root = os.getenv('BEADROOT')
    fire.Fire(Cli)
