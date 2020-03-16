from canvas import BeadCanvas
from layout import BeadLayout
from palette import BeadColor, BeadPalette
from io import StringIO


def test_rectangles():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 2)
    sut = create_sut(layout, 4)

    assert len(sut.rectangles) == 2
    assert sut.rectangles[0] == (0, 0, 3, 4)
    assert sut.rectangles[1] == (0, 4, 3, 3)


def test_circles():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    layout.set_value(0, 2, 'BLU')
    sut = create_sut(layout, 10)

    assert len(sut.circles) == 2
    assert sut.circles[0] == (2, 2, 6, '#aaaaaa', '#aaaaaa')
    assert sut.circles[1] == (2, 22, 6, '#bbbbbb', '#bbbbbb')


def test_circles_white():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'WHT')
    layout.set_value(0, 2, 'WHT')
    sut = create_sut(layout, 10)

    assert len(sut.circles) == 2
    assert sut.circles[0] == (2, 2, 6, '#000000', '#cccccc')
    assert sut.circles[1] == (2, 22, 6, '#000000', '#cccccc')


def test_try_set_edge():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    sut = create_sut(layout, 10)

    sut.try_set(0, 1, 'RED')
    sut.try_set(0, 10, 'RED')

    assert len(sut.circles) == 0


def test_try_set_valid():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    sut = create_sut(layout, 10)

    sut.try_set(1, 1, 'RED')

    assert len(sut.circles) == 1
    assert sut.circles[0] == (2, 2, 6, '#aaaaaa', '#aaaaaa')


def test_try_set_overwrite():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    sut = create_sut(layout, 10)

    sut.try_set(1, 1, 'RED')
    sut.try_set(1, 1, 'WHT')

    assert len(sut.circles) == 1
    assert sut.circles[0] == (2, 2, 6, '#aaaaaa', '#aaaaaa')


def test_try_clear_edge():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 10)

    sut.try_clear(1, 0)

    assert len(sut.circles) == 1
    assert sut.circles[0] == (2, 2, 6, '#aaaaaa', '#aaaaaa')


def test_try_clear_valid():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 10)

    sut.try_clear(1, 1)

    assert len(sut.circles) == 0


def test_layout():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 10)

    assert sut.layout.get_value(0, 0) == 'RED'


def create_pseudo_file(raw_json):
    f = StringIO()
    f.write(raw_json)
    f.seek(0)

    return f


def create_palette():
    c1 = BeadColor('01', 'RED', 'Red', '#aaaaaa')
    c2 = BeadColor('02', 'BLU', 'Blue', '#bbbbbb')
    c3 = BeadColor('03', 'WHT', 'White', '#cccccc')
    return BeadPalette([c1, c2, c3])


def create_sut(layout, cell_size):
    palette = create_palette()
    return BeadCanvas(layout, palette, cell_size)