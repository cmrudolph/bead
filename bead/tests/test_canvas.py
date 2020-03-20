from bead import Canvas, Color, Layout, Palette
from io import StringIO


def test_rectangles():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 2)
    sut = create_sut(layout, 4)

    assert len(sut.rectangles) == 2

    r1 = sut.rectangles[0]
    assert r1.topleft == (0, 0)
    assert r1.bottomright == (3, 4)
    assert r1.width == 3
    assert r1.height == 4

    r2 = sut.rectangles[1]
    assert r2.topleft == (0, 4)
    assert r2.bottomright == (3, 7)
    assert r2.width == 3
    assert r2.height == 3


def test_circles():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    layout.set_value(0, 2, 'BLU')
    sut = create_sut(layout, 10)

    assert len(sut.circles) == 2

    c1 = sut.circles[0]
    assert c1.topleft == (2, 2)
    assert c1.bottomright == (8, 8)
    assert c1.diameter == 6
    assert c1.fill_color == '#aaaaaa'
    assert c1.edge_color == '#aaaaaa'

    c2 = sut.circles[1]
    assert c2.topleft == (2, 22)
    assert c2.bottomright == (8, 28)
    assert c2.diameter == 6
    assert c2.fill_color == '#bbbbbb'
    assert c2.edge_color == '#bbbbbb'


def test_circles_white():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'WHT')
    layout.set_value(0, 2, 'WHT')
    sut = create_sut(layout, 10)

    c1 = sut.circles[0]
    assert c1.fill_color == '#cccccc'
    assert c1.edge_color == '#000000'

    c2 = sut.circles[1]
    assert c2.fill_color == '#cccccc'
    assert c2.edge_color == '#000000'


def test_try_set_edge():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    sut = create_sut(layout, 10)

    sut.try_set(0, 1, 'RED')
    sut.try_set(0, 10, 'RED')

    assert len(sut.circles) == 0


def test_try_set_valid():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    sut = create_sut(layout, 10)

    sut.try_set(1, 1, 'RED')

    assert len(sut.circles) == 1

    c1 = sut.circles[0]
    assert c1.fill_color == '#aaaaaa'
    assert c1.edge_color == '#aaaaaa'


def test_try_set_overwrite():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    sut = create_sut(layout, 10)

    sut.try_set(1, 1, 'RED')
    sut.try_set(1, 1, 'WHT')

    assert len(sut.circles) == 1

    c1 = sut.circles[0]
    assert c1.fill_color == '#aaaaaa'
    assert c1.edge_color == '#aaaaaa'


def test_try_clear_edge():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 10)

    sut.try_clear(1, 0)

    assert len(sut.circles) == 1

    c1 = sut.circles[0]
    assert c1.fill_color == '#aaaaaa'
    assert c1.edge_color == '#aaaaaa'


def test_try_clear_valid():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 10)

    sut.try_clear(1, 1)

    assert len(sut.circles) == 0


def test_layout():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 10)

    assert sut.layout.get_value(0, 0) == 'RED'


def create_pseudo_file(raw_json):
    f = StringIO()
    f.write(raw_json)
    f.seek(0)

    return f


def create_palette():
    c1 = Color('01', 'RED', 'Red', '#aaaaaa')
    c2 = Color('02', 'BLU', 'Blue', '#bbbbbb')
    c3 = Color('03', 'WHT', 'White', '#cccccc')
    return Palette([c1, c2, c3])


def create_sut(layout, cell_size):
    palette = create_palette()
    return Canvas(layout, palette, cell_size)
