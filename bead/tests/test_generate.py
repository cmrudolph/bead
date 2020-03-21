from . import utils
from bead import Project, generate_layout
import filecmp
import os
import pytest
import shutil


def test_generate_transparency(tmpdir):
    baseline_path = baseline('transparency_layout.txt')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    src = misc('transparency.png')
    dest = p.quantized_path
    shutil.copyfile(src, dest)

    generate_layout(p)

    assert filecmp.cmp(baseline_path, p.layout_path) is True


def test_generate_notransparency(tmpdir):
    baseline_path = baseline('notransparency_layout.txt')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    src = misc('notransparency.png')
    dest = p.quantized_path
    shutil.copyfile(src, dest)

    generate_layout(p)

    assert filecmp.cmp(baseline_path, p.layout_path) is True


def test_generate_exists_noforce(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)
    src = misc('transparency.png')
    dest = p.quantized_path
    shutil.copyfile(src, dest)

    generate_layout(p)
    with pytest.raises(ValueError):
        generate_layout(p)


def test_generate_exists_force(tmpdir):
    baseline_path = baseline('transparency_layout.txt')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    src = misc('transparency.png')
    dest = p.quantized_path
    shutil.copyfile(src, dest)

    generate_layout(p)
    generate_layout(p, force=True)

    assert filecmp.cmp(baseline_path, p.layout_path) is True


def test_generate_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)

    with pytest.raises(ValueError):
        generate_layout(p)


def baseline(file_name):
    return utils.get_baseline_path('test_generate', file_name)


def misc(file_name):
    return utils.get_misc_path('test_generate', file_name)
