from . import utils
from bead import Project, crop_image
import filecmp
import os
import pytest
import shutil


def test_crop_transparent_edges(tmpdir):
    baseline_path = baseline('transparent_edges_cropped.png')
    p = utils.create_project(tmpdir, 'p', 10, 10)
    shutil.copyfile(misc('transparent_edges.png'), p.orig_path)

    crop_image(p)

    assert filecmp.cmp(baseline_path, p.cropped_path) is True


def test_crop_no_transparent_edges(tmpdir):
    baseline_path = baseline('no_transparent_edges_cropped.png')
    p = utils.create_project(tmpdir, 'p', 10, 10)
    shutil.copyfile(misc('no_transparent_edges.png'), p.orig_path)

    crop_image(p)

    assert filecmp.cmp(baseline_path, p.cropped_path) is True


def test_export_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)

    with pytest.raises(ValueError):
        crop_image(p)


def baseline(file_name):
    return utils.get_baseline_path('test_crop', file_name)


def misc(file_name):
    return utils.get_misc_path('test_crop', file_name)
