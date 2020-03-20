import fire
import os
from bead import generate_layout


Root = None


class Cli():
    def generate(self, project_name):
        project = Project(Root, project_name)
        generate_layout(project)


if __name__ == "__main__":
    Root = os.getenv('BEADROOT')
    fire.Fire(Cli)
