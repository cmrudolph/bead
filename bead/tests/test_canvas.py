from bead import Canvas, Color, Layout, Palette
from io import StringIO


def test_lines():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 2, 3)
    sut = create_sut(layout, 5)

    print()
    for line in sut.lines:
        print(f'({line.point1}) -> {line.point2}')

    assert len(sut.lines) == 3

    line1 = sut.lines[0]
    assert line1.point1 == (5, 0)
    assert line1.point2 == (5, 17)

    line2 = sut.lines[1]
    assert line2.point1 == (0, 5)
    assert line2.point2 == (11, 5)

    line3 = sut.lines[2]
    assert line3.point1 == (0, 11)
    assert line3.point2 == (11, 11)


def test_circles():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    layout.set_value(0, 2, 'BLU')
    sut = create_sut(layout, 9)

    assert len(sut.circles) == 2

    c1 = sut.circles[0]
    assert c1.topleft == (1, 1)
    assert c1.bottomright == (7, 7)
    assert c1.diameter == 6
    assert c1.fill_color == '#222222'
    assert c1.edge_color == '#333333'

    c2 = sut.circles[1]
    assert c2.topleft == (1, 21)
    assert c2.bottomright == (7, 27)
    assert c2.diameter == 6
    assert c2.fill_color == '#555555'
    assert c2.edge_color == '#666666'


def test_height():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 2, 3)
    sut = create_sut(layout, 5)

    assert sut.height == 17


def test_width():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 2, 3)
    sut = create_sut(layout, 5)

    assert sut.width == 11


def test_try_set_edge():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 2, 3)
    sut = create_sut(layout, 9)

    sut.try_set(9, 0, 'RED')
    sut.try_set(0, 9, 'RED')

    assert len(sut.circles) == 0


def test_try_set_valid():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    sut = create_sut(layout, 9)

    sut.try_set(0, 0, 'RED')

    assert len(sut.circles) == 1

    c1 = sut.circles[0]
    assert c1.fill_color == '#222222'
    assert c1.edge_color == '#333333'


def test_try_set_overwrite():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    sut = create_sut(layout, 9)

    sut.try_set(1, 1, 'RED')
    sut.try_set(1, 1, 'WHT')

    assert len(sut.circles) == 1

    c1 = sut.circles[0]
    assert c1.fill_color == '#222222'
    assert c1.edge_color == '#333333'


def test_try_clear_edge():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 9)

    sut.try_clear(9, 0)

    assert len(sut.circles) == 1

    c1 = sut.circles[0]
    assert c1.fill_color == '#222222'
    assert c1.edge_color == '#333333'


def test_try_clear_valid():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 9)

    sut.try_clear(0, 0)

    assert len(sut.circles) == 0


def test_layout():
    f = create_pseudo_file('')
    layout = Layout.create_new(f, 1, 3)
    layout.set_value(0, 0, 'RED')
    sut = create_sut(layout, 9)

    assert sut.layout.get_value(0, 0) == 'RED'


def create_pseudo_file(raw_json):
    f = StringIO()
    f.write(raw_json)
    f.seek(0)

    return f


def create_palette():
    c1 = Color('01', 'RED', 'Red', '#111111', '#222222', '#333333')
    c2 = Color('02', 'BLU', 'Blue', '#444444', '#555555', '#666666')
    c3 = Color('03', 'WHT', 'White', '#777777', '#888888', '#999999')
    return Palette([c1, c2, c3])


def create_sut(layout, cell_size):
    palette = create_palette()
    return Canvas(layout, palette, cell_size)
