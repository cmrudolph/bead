from . import utils
from bead import Project, generate_layout
import filecmp
import os
import pytest


def test_generate_transparency(tmpdir):
    baseline_path = utils.get_baseline_path('generate.txt')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    utils.copy_input('generate.png', p.quantized_path)

    generate_layout(p)

    assert filecmp.cmp(baseline_path, p.layout_path) is True


def test_generate_exists_noforce(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)
    utils.copy_input('generate.png', p.quantized_path)

    generate_layout(p)
    with pytest.raises(ValueError):
        generate_layout(p)


def test_generate_exists_force(tmpdir):
    baseline_path = utils.get_baseline_path('generate.txt')
    p = utils.create_project(tmpdir, 'p', 2, 2)
    utils.copy_input('generate.png', p.quantized_path)

    generate_layout(p)
    generate_layout(p, force=True)

    assert filecmp.cmp(baseline_path, p.layout_path) is True


def test_generate_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 2, 2)

    with pytest.raises(ValueError):
        generate_layout(p)
