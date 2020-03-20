from bead import Project
import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_project_valid():
    root = os.path.join(DATA_DIR, 'projects')
    sut = Project(root, 'test_project')

    assert sut.name == 'test_project'
    assert sut.properties.width == 29
    assert sut.palette.color_from_code('WHT').name == 'White'

    assert 'test_project' in sut.orig_path
    assert 'original.png' in sut.orig_path

    assert 'test_project' in sut.quantized_path
    assert 'quantized.png' in sut.quantized_path

    assert 'test_project' in sut.partitioned_path
    assert 'partitioned.png' in sut.partitioned_path

    assert 'test_project' in sut.layout_path
    assert 'layout.txt' in sut.layout_path

    assert 'test_project' in sut.final_path
    assert 'final.png' in sut.final_path


def test_project_missing_root():
    root = os.path.join(DATA_DIR, 'projects', 'foo')

    with pytest.raises(ValueError):
        sut = Project(root, 'test_project')
