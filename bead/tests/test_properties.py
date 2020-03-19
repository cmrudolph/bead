import json
import pytest
from bead import BeadProperties
from io import StringIO


Txt = '{"width":29,"height":26,"quantize_colors":20,"colors":["A", "B"]}'


def test_load_from_json():
    sut = BeadProperties.load_from_json(Txt)
    _assert_common(sut)


def test_load_from_file():
    f = _create_pseudo_file(Txt)
    sut = BeadProperties.load_from_file(f)
    _assert_common(sut)


def test_load_from_dict():
    d = json.loads(Txt)
    sut = BeadProperties.load_from_dict(d)
    _assert_common(sut)


def _assert_common(sut):
    assert sut.width == 29
    assert sut.height == 26
    assert sut.quantize_colors == 20
    assert sut.colors == ['A', 'B']


def _create_pseudo_file(raw_txt):
    f = StringIO()
    f.write(raw_txt)
    f.seek(0)

    return f
