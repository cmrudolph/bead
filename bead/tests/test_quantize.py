from . import utils
from bead import Project, quantize_image
import filecmp
import os
import pytest
import shutil


def test_quantize_notransparency(tmpdir):
    baseline_path = baseline('notransparency_quantized.png')
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)
    shutil.copyfile(misc('notransparency.png'), p.orig_path)

    quantize_image(p)

    assert filecmp.cmp(baseline_path, p.quantized_path) is True


def test_quantize_transparency(tmpdir):
    baseline_path = baseline('transparency_quantized.png')
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)
    shutil.copyfile(misc('transparency.png'), p.orig_path)

    quantize_image(p)

    assert filecmp.cmp(baseline_path, p.quantized_path) is True


def test_quantize_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)

    with pytest.raises(ValueError):
        quantize_image(p)


def baseline(file_name):
    return utils.get_baseline_path('test_quantize', file_name)


def misc(file_name):
    return utils.get_misc_path('test_quantize', file_name)
