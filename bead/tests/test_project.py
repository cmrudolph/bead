from bead import Project
import os
import pytest
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
NAME = 'test_project'


@pytest.fixture
def root_dir(tmpdir):
    source_dir = os.path.join(DATA_DIR, 'projects', NAME)
    shutil.copytree(source_dir, tmpdir.join(NAME))
    print(f'\nTest project -- Root:{tmpdir}; Name:{NAME}')
    return tmpdir


def test_project_valid(root_dir):
    sut = Project(root_dir, NAME)

    assert sut.name == NAME
    assert sut.properties.width == 29
    assert sut.palette.color_from_code('WHT').name == 'White'
    assert len(sut.palette.colors) == 39

    assert NAME in sut.orig_path
    assert 'original.png' in sut.orig_path

    assert NAME in sut.quantized_path
    assert 'quantized.png' in sut.quantized_path

    assert NAME in sut.partitioned_path
    assert 'partitioned.png' in sut.partitioned_path

    assert NAME in sut.layout_path
    assert 'layout.txt' in sut.layout_path

    assert NAME in sut.final_path
    assert 'final.png' in sut.final_path


def test_project_filtered_colors(root_dir):
    colors_file = os.path.join(root_dir, NAME, 'colors.txt')
    with open(colors_file, 'w') as f:
        f.write('Black\nWhite')

    sut = Project(root_dir, NAME)

    assert len(sut.palette.colors) == 2
    assert sut.palette.color_from_code('WHT').name == 'White'
    assert sut.palette.color_from_code('BLK').name == 'Black'
    assert sut.palette.color_from_code('RED') is None


def test_project_missing_root():
    root = os.path.join(DATA_DIR, 'projects', 'foo')

    with pytest.raises(ValueError):
        sut = Project(root, NAME)
