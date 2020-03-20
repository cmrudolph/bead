import fire
import os
from bead import Project, export_layout


Root = None


class Cli():
    def export(self, project_name):
        project = Project(Root, project_name)
        export_layout(project)


if __name__ == "__main__":
    Root = os.getenv('BEADROOT')
    fire.Fire(Cli)
