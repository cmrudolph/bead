from . import utils
from bead import Project, crop_image
import filecmp
import os
import pytest


def test_crop_transparent_edges(tmpdir):
    baseline_path = utils.get_baseline_path('crop_needs_crop.png')
    p = utils.create_project(tmpdir, 'p', 10, 10)
    utils.copy_input('crop_needs_crop.png', p.orig_path)

    crop_image(p)

    assert filecmp.cmp(baseline_path, p.cropped_path) is True


def test_crop_no_transparent_edges(tmpdir):
    baseline_path = utils.get_baseline_path('crop_noop.png')
    p = utils.create_project(tmpdir, 'p', 10, 10)
    utils.copy_input('crop_noop.png', p.orig_path)

    crop_image(p)

    assert filecmp.cmp(baseline_path, p.cropped_path) is True


def test_export_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)

    with pytest.raises(ValueError):
        crop_image(p)
