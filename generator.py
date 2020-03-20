import fire
import os
from bead import Project, generate_layout


Root = None


class Cli():
    def generate(self, project_name, force=False):
        project = Project(Root, project_name)
        generate_layout(project, force)


if __name__ == "__main__":
    Root = os.getenv('BEADROOT')
    fire.Fire(Cli)
