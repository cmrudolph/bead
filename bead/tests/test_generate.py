from bead import Project, generate_layout
import filecmp
import os
import pytest
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MISC_DIR = os.path.join(DATA_DIR, 'misc', 'test_generate')
BASELINES_DIR = os.path.join(DATA_DIR, 'baselines', 'test_generate')


@pytest.fixture
def project(tmpdir):
    name = 'test_generate'
    source_dir = os.path.join(DATA_DIR, 'projects', name)
    shutil.copytree(source_dir, tmpdir.join(name))
    print(f'\nTest project -- Root:{tmpdir}; Name:{name}')
    return Project(tmpdir, name)


def test_generate_transparency(project):
    baseline_path = os.path.join(BASELINES_DIR, 'transparency_layout.txt')

    generate_layout(project)
    assert filecmp.cmp(baseline_path, project.layout_path) is True


def test_generate_notransparency(project):
    baseline_path = os.path.join(BASELINES_DIR, 'notransparency_layout.txt')
    src = os.path.join(MISC_DIR, 'notransparency.png')
    shutil.copyfile(src, project.quantized_path)

    generate_layout(project)
    assert filecmp.cmp(baseline_path, project.layout_path) is True


def test_generate_exists_noforce(project):
    baseline_path = os.path.join(BASELINES_DIR, 'transparency_layout.txt')

    generate_layout(project)
    with pytest.raises(ValueError):
        generate_layout(project)


def test_generate_exists_force(project):
    baseline_path = os.path.join(BASELINES_DIR, 'transparency_layout.txt')

    generate_layout(project)
    generate_layout(project, force=True)
    assert filecmp.cmp(baseline_path, project.layout_path) is True


def test_generate_missing_input(project):
    os.unlink(project.quantized_path)

    with pytest.raises(ValueError):
        generate_layout(project)
