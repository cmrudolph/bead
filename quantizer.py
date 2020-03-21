import fire
import os
from bead import Project, quantize_image


Root = None


class Cli():
    def quantize(self, project_name):
        project = Project(Root, project_name)
        quantize_image(project)


if __name__ == "__main__":
    Root = os.getenv('BEADROOT')
    fire.Fire(Cli)
