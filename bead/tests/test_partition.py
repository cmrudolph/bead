from . import utils
from bead import Project, partition_image
import filecmp
import os
import pytest


def test_crop_noop(tmpdir):
    baseline_path = utils.get_baseline_path('crop_noop.png')
    p = utils.create_project(tmpdir, 'p', 1, 1, 3)
    utils.copy_input('crop_noop.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline_path, p.partitioned_path) is True


def test_crop_notrans(tmpdir):
    baseline_path = utils.get_baseline_path('crop_notrans.png')
    p = utils.create_project(tmpdir, 'p', 1, 1, 3)
    utils.copy_input('crop_notrans.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline_path, p.partitioned_path) is True


def test_crop_needs_crop(tmpdir):
    baseline_path = utils.get_baseline_path('crop_needs_crop.png')
    p = utils.create_project(tmpdir, 'p', 1, 1, 3)
    utils.copy_input('crop_needs_crop.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline_path, p.partitioned_path) is True


def test_scale_no_scale(tmpdir):
    baseline_path = utils.get_baseline_path('scale_no_scale.png')
    p = utils.create_project(tmpdir, 'p', 2, 2, 3)
    utils.copy_input('scale_no_scale.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline_path, p.partitioned_path) is True


def test_scale_needs_scale(tmpdir):
    baseline_path = utils.get_baseline_path('scale_needs_scale.png')
    p = utils.create_project(tmpdir, 'p', 2, 2, 3)
    utils.copy_input('scale_needs_scale.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline_path, p.partitioned_path) is True


def test_gridify_every_pixel(tmpdir):
    baseline1 = utils.get_baseline_path('gridify_every_pixel_trans.png')
    baseline2 = utils.get_baseline_path('gridify_every_pixel_color.png')
    p = utils.create_project(tmpdir, 'p', 4, 4, 3)
    utils.copy_input('gridify_every_pixel.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline1, p.partitioned_path) is True
    assert filecmp.cmp(baseline2, p.gridified_path) is True


def test_gridify_groups(tmpdir):
    baseline1 = utils.get_baseline_path('gridify_groups_trans.png')
    baseline2 = utils.get_baseline_path('gridify_groups_color.png')
    p = utils.create_project(tmpdir, 'p', 2, 2, 3)
    utils.copy_input('gridify_groups.png', p.orig_path)

    partition_image(p)

    assert filecmp.cmp(baseline1, p.partitioned_path) is True
    assert filecmp.cmp(baseline2, p.gridified_path) is True


def test_partition_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)

    with pytest.raises(ValueError):
        partition_image(p)
