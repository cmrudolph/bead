from . import utils
from bead import Layout, Project, export_layout
import filecmp
import os
import pytest


def test_export_valid(tmpdir):
    baseline_path = utils.get_baseline_path('export_valid.png')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    with open(p.layout_path, 'w') as f:
        layout = Layout.create_new(f, 2, 2)
        layout.set_value(0, 0, 'BLK')
        layout.set_value(1, 0, 'WHT')
        layout.set_value(0, 1, 'BLK')

    export_layout(p)

    assert filecmp.cmp(baseline_path, p.final_path) is True


def test_export_overwrite(tmpdir):
    baseline_path = utils.get_baseline_path('export_valid.png')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    with open(p.layout_path, 'w') as f:
        layout = Layout.create_new(f, 2, 2)
        layout.set_value(0, 0, 'BLK')
        layout.set_value(1, 0, 'WHT')
        layout.set_value(0, 1, 'BLK')

    export_layout(p)
    export_layout(p)

    assert filecmp.cmp(baseline_path, p.final_path) is True


def test_export_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)

    with pytest.raises(ValueError):
        export_layout(p)


def test_export_width_mismatch(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)
    with open(p.layout_path, 'w') as f:
        layout = Layout.create_new(f, 1, 2)

    with pytest.raises(ValueError):
        export_layout(p)


def test_export_height_mismatch(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)
    with open(p.layout_path, 'w') as f:
        layout = Layout.create_new(f, 2, 1)

    with pytest.raises(ValueError):
        export_layout(p)
