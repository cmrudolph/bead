from . import utils
from bead import clean_project
import os


def test_clean_nocommit(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)
    _prepare_test_project(p)

    clean_project(p)

    files = os.listdir(p.project_dir)
    assert len(files) == 7


def test_clean_commit(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)
    _prepare_test_project(p)

    clean_project(p, commit=True)

    files = os.listdir(p.project_dir)
    assert len(files) == 3
    assert 'original.png' in files
    assert 'properties.json' in files
    assert 'layout.txt' in files


def _prepare_test_project(p):
    with open(p.properties_path, 'w') as f:
        f.write('A')
    with open(p.orig_path, 'w') as f:
        f.write('A')
    with open(p.gridified_path, 'w') as f:
        f.write('A')
    with open(p.partitioned_path, 'w') as f:
        f.write('A')
    with open(p.quantized_path, 'w') as f:
        f.write('A')
    with open(p.layout_path, 'w') as f:
        f.write('A')
    with open(os.path.join(p.project_dir, 'foo.txt'), 'w') as f:
        f.write('A')
