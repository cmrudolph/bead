from bead import Layout
from io import StringIO


def test_create_new():
    f = create_pseudo_file('')
    sut = Layout.create_new(f, 3, 2)

    assert sut.width == 3
    assert sut.height == 2
    assert sut.values == [[None, None, None], [None, None, None]]

    verify_result(sut, f, 3, 2, [[None, None, None], [None, None, None]])


def test_create_from_file_none():
    s = '1|1\n---'
    f = create_pseudo_file(s)
    sut = Layout.load_from_file(f)

    verify_result(sut, f, 1, 1, [[None]])


def test_create_from_file_not_none():
    s = '1|1\nRED'
    f = create_pseudo_file(s)
    sut = Layout.load_from_file(f)

    verify_result(sut, f, 1, 1, [['RED']])


def test_create_from_file_wide():
    s = '2|1\n---|RED'
    f = create_pseudo_file(s)
    sut = Layout.load_from_file(f)

    verify_result(sut, f, 2, 1, [[None, 'RED']])


def test_create_from_file_tall():
    s = '1|2\n---\nRED'
    f = create_pseudo_file(s)
    sut = Layout.load_from_file(f)

    verify_result(sut, f, 1, 2, [[None], ['RED']])


def test_set_value():
    f = create_pseudo_file('')
    sut = Layout.create_new(f, 1, 2)

    sut.set_value(0, 1, 'BLU')

    assert sut.get_value(0, 1) == 'BLU'
    verify_result(sut, f, 1, 2, [[None], ['BLU']])


def test_clear_value():
    f = create_pseudo_file('')
    sut = Layout.create_new(f, 1, 2)

    sut.set_value(0, 1, 'BLU')
    sut.clear_value(0, 1)

    assert sut.get_value(0, 1) is None
    verify_result(sut, f, 1, 2, [[None], [None]])


def verify_result(sut, f, width, height, values):
    f.seek(0)
    actual = Layout.load_from_file(f)

    # Verify the state of the object under test
    assert sut.width == width
    assert sut.height == height
    assert sut.values == values

    # Also verify the backing file to ensure coherence
    assert actual.width == width
    assert actual.height == height
    assert actual.values == values


def create_pseudo_file(raw_txt):
    f = StringIO()
    f.write(raw_txt)
    f.seek(0)

    return f
