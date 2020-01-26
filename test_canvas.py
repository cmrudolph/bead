from canvas import BeadCanvas
from layout import BeadLayout
from io import StringIO


def test_rectangles():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 2)
    sut = BeadCanvas(layout, 4)

    assert len(sut.rectangles) == 2
    assert sut.rectangles[0] == (0, 0, 3, 4)
    assert sut.rectangles[1] == (0, 4, 3, 3)


def test_circles():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, '#ffffff')
    layout.set_value(0, 2, '#111111')
    sut = BeadCanvas(layout, 10)

    assert len(sut.circles) == 2
    assert sut.circles[0] == (2, 2, 6, '#000000', '#ffffff')
    assert sut.circles[1] == (2, 22, 6, '#111111', '#111111')


def test_try_set_edge():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    sut = BeadCanvas(layout, 10)

    sut.try_set(0, 1, '#cccccc')
    sut.try_set(0, 10, '#cccccc')

    assert len(sut.circles) == 0


def test_try_set_valid():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    sut = BeadCanvas(layout, 10)

    sut.try_set(1, 1, '#cccccc')

    assert len(sut.circles) == 1
    assert sut.circles[0] == (2, 2, 6, '#cccccc', '#cccccc')


def test_try_set_overwrite():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    sut = BeadCanvas(layout, 10)

    sut.try_set(1, 1, '#cccccc')
    sut.try_set(1, 1, '#bbbbbb')

    assert len(sut.circles) == 1
    assert sut.circles[0] == (2, 2, 6, '#cccccc', '#cccccc')


def test_try_clear_edge():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, '#cccccc')
    sut = BeadCanvas(layout, 10)

    sut.try_clear(1, 0)

    assert len(sut.circles) == 1
    assert sut.circles[0] == (2, 2, 6, '#cccccc', '#cccccc')


def test_try_clear_valid():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, '#cccccc')
    sut = BeadCanvas(layout, 10)

    sut.try_clear(1, 1)

    assert len(sut.circles) == 0


def test_layout():
    f = create_pseudo_file('')
    layout = BeadLayout.create_new(f, 1, 3)
    layout.set_value(0, 0, '#cccccc')
    sut = BeadCanvas(layout, 10)

    assert sut.layout.get_value(0, 0) == '#cccccc'


def create_pseudo_file(raw_json):
    f = StringIO()
    f.write(raw_json)
    f.seek(0)

    return f
