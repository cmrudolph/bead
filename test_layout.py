from layout import BeadLayout
from io import StringIO


def test_create_new():
    f = create_pseudo_file('')
    sut = BeadLayout.create_new(f, 3, 2)

    assert sut.width == 3
    assert sut.height == 2
    assert sut.values == [None] * 6

    verify_result(sut, f, 3, 2, [None] * 6)


def test_create_from_file():
    s = '{"width":1,"height":2,"values":["#aaaaaa", "#bbbbbb"]}'
    f = create_pseudo_file(s)
    sut = BeadLayout.create_from_file(f)

    verify_result(sut, f, 1, 2, ['#aaaaaa', '#bbbbbb'])


def test_set_value():
    f = create_pseudo_file('')
    sut = BeadLayout.create_new(f, 1, 2)

    sut.set_value(0, 1, '#aaaaaa')

    assert sut.get_value(0, 1) == '#aaaaaa'
    verify_result(sut, f, 1, 2, [None, '#aaaaaa'])


def test_clear_value():
    f = create_pseudo_file('')
    sut = BeadLayout.create_new(f, 1, 2)

    sut.set_value(0, 1, '#aaaaaa')
    sut.clear_value(0, 1)

    assert sut.get_value(0, 1) is None
    verify_result(sut, f, 1, 2, [None, None])


def test_replace_values():
    f = create_pseudo_file('')
    sut = BeadLayout.create_new(f, 1, 3)

    sut.set_value(0, 0, '#ffffff')
    sut.set_value(0, 1, '#dddddd')
    sut.set_value(0, 2, '#ffffff')
    sut.replace_values('#ffffff', '#cccccc')

    verify_result(sut, f, 1, 3, ['#cccccc', '#dddddd', '#cccccc'])


def verify_result(sut, f, width, height, values):
    f.seek(0)
    actual = BeadLayout.create_from_file(f)

    # Verify the state of the object under test
    assert sut.width == width
    assert sut.height == height
    assert sut.values == values

    # Also verify the backing file to ensure coherence
    assert actual.width == width
    assert actual.height == height
    assert actual.values == values


def create_pseudo_file(raw_json):
    f = StringIO()
    f.write(raw_json)
    f.seek(0)

    return f
