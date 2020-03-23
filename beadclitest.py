import fire
import os
from bead import Project
from beadcli import Cli as RealCli


def delete_file(path):
    if os.path.exists(path):
        print(f'Deleting file -- Path:{path}')
        os.unlink(path)


class Cli():
    def __init__(self):
        self._root = os.getenv('BEADROOT')

    def clean(self):
        partitioned = Project(os.path.join(self._root, 'test_partitioned'))
        delete_file(partitioned.partitioned_path)
        delete_file(partitioned.gridified_path)

        export = Project(os.path.join(self._root, 'test_export'))
        delete_file(export.final_path)

        generate = Project(os.path.join(self._root, 'test_generate'))
        delete_file(generate.layout_path)

        quantize = Project(os.path.join(self._root, 'test_quantize'))
        delete_file(quantize.quantized_path)

    def runall(self):
        real = RealCli()

        real.partition('test_partition')
        real.export('test_export')
        real.generate('test_generate')
        real.quantize('test_quantize')


if __name__ == "__main__":
    fire.Fire(Cli)
