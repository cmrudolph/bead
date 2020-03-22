from . import utils
from bead import Project
import os
import pytest


def test_project_valid(tmpdir):
    name = 'p888'
    pf = utils.create_project_folder(tmpdir, name, 29, 26, 20)
    sut = Project(pf)

    assert sut.name == name
    assert sut.properties.width == 29
    assert sut.palette.color_from_code('WHT').name == 'White'
    assert len(sut.palette.colors) == 39

    assert name in sut.orig_path
    assert 'original.png' in sut.orig_path

    assert name in sut.gridified_path
    assert 'gridified.png' in sut.gridified_path

    assert name in sut.partitioned_path
    assert 'partitioned.png' in sut.partitioned_path

    assert name in sut.quantized_path
    assert 'quantized.png' in sut.quantized_path

    assert name in sut.layout_path
    assert 'layout.txt' in sut.layout_path

    assert name in sut.final_path
    assert 'final.png' in sut.final_path


def test_project_filtered_colors(tmpdir):
    whitelist = ['White', 'Black']
    pf = utils.create_project_folder(tmpdir, 'p', 1, 1, colors=whitelist)
    sut = Project(pf)

    assert len(sut.palette.colors) == 2
    assert sut.palette.color_from_code('WHT').name == 'White'
    assert sut.palette.color_from_code('BLK').name == 'Black'
    assert sut.palette.color_from_code('RED') is None


def test_project_none_dir():
    with pytest.raises(ValueError):
        sut = Project(None)


def test_project_missing_dir(tmpdir):
    pf = os.path.join(tmpdir, 'foo')

    with pytest.raises(ValueError):
        sut = Project(pf)


def test_project_missing_properties(tmpdir):
    pf = os.path.join(tmpdir, 'foo')
    os.mkdir(pf)

    with pytest.raises(ValueError):
        sut = Project(pf)
