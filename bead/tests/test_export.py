from bead import Layout, Project, export_layout
import filecmp
import os
import pytest
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
BASELINES_DIR = os.path.join(DATA_DIR, 'baselines', 'test_export')


@pytest.fixture
def project(tmpdir):
    name = 'test_export'
    source_dir = os.path.join(DATA_DIR, 'projects', name)
    shutil.copytree(source_dir, tmpdir.join(name))
    print(f'\nTest project -- Root:{tmpdir}; Name:{name}')
    return Project(tmpdir, name)


def test_export_valid(project):
    baseline_path = os.path.join(BASELINES_DIR, 'valid_final.png')

    export_layout(project)
    assert filecmp.cmp(baseline_path, project.final_path) is True


def test_export_overwrite(project):
    baseline_path = os.path.join(BASELINES_DIR, 'valid_final.png')

    export_layout(project)
    export_layout(project)
    assert filecmp.cmp(baseline_path, project.final_path) is True


def test_export_missing_input(project):
    os.unlink(project.layout_path)

    with pytest.raises(ValueError):
        export_layout(project)


def test_export_width_mismatch(project):
    os.unlink(project.layout_path)
    with open(project.layout_path, 'w') as f:
        layout = Layout.create_new(f, 1, 2)

    with pytest.raises(ValueError):
        export_layout(project)


def test_export_height_mismatch(project):
    os.unlink(project.layout_path)
    with open(project.layout_path, 'w') as f:
        layout = Layout.create_new(f, 2, 1)

    with pytest.raises(ValueError):
        export_layout(project)
