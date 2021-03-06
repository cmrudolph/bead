from . import utils
from bead import quantize_image
import filecmp
import pytest


def test_quantize_notransparency(tmpdir):
    baseline_path = utils.get_baseline_path('quantize_notransparency.png')
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)
    utils.copy_input('quantize_notransparency.png', p.partitioned_path)

    quantize_image(p)

    assert filecmp.cmp(baseline_path, p.quantized_path) is True


def test_quantize_transparency(tmpdir):
    baseline_path = utils.get_baseline_path('quantize_transparency.png')
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)
    utils.copy_input('quantize_transparency.png', p.partitioned_path)

    quantize_image(p)

    assert filecmp.cmp(baseline_path, p.quantized_path) is True


def test_quantize_missing_input(tmpdir):
    p = utils.create_project(tmpdir, 'p', 50, 50, 3)

    with pytest.raises(ValueError):
        quantize_image(p)
