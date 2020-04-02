import pytest
from bead import Palette, Color
from io import StringIO


closest_color_rgb_cases = [
    ('#000000', 'BLK'),
    ('#242224', 'BLK'),
    ('#343234', 'BLK'),
    ('#444244', 'BLK'),
    ('#e7e7e2', 'WHT'),
    ('#f7f7f2', 'WHT'),
    ('#ffffff', 'WHT'),
    ('#b42a34', 'RED'),
    ('#c43a44', 'RED'),
    ('#d44a54', 'RED'),
    ('#00867a', 'PGR'),
    ('#00968a', 'PGR'),
    ('#10a69a', 'PGR'),
    ('#0056a3', 'CBT'),
    ('#0066b3', 'CBT'),
    ('#1076c3', 'CBT')
]


def test_create_from_txt():
    raw = ('ID | CODE | NAME | INT | VIEW | EDGE\n'
           '02 | RED | Red  | #111111 | | #333333\n\n'
           '01 | BLU | Blue | #444444 | #555555 | \n\n')
    sut = Palette.create_from_txt(raw)

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Red', 'Blue']
    assert [c.hex_internal for c in sut.colors] == ['#111111', '#444444']
    assert [c.hex_view for c in sut.colors] == ['#111111', '#555555']
    assert [c.hex_edge for c in sut.colors] == ['#333333', '#444444']


def test_create_from_file():
    raw = ('ID | CODE | NAME | INT | VIEW | EDGE\n'
           '02 | RED | Red  | #111111 | | #333333\n\n'
           '01 | BLU | Blue | #444444 | #555555 | \n\n')
    f = create_pseudo_file(raw)
    sut = Palette.create_from_file(f)

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Red', 'Blue']
    assert [c.hex_internal for c in sut.colors] == ['#111111', '#444444']
    assert [c.hex_view for c in sut.colors] == ['#111111', '#555555']
    assert [c.hex_edge for c in sut.colors] == ['#333333', '#444444']


def test_construct_directly():
    sut = create_sut()

    assert [c.id for c in sut.colors] == ['16', '02', '42', '17', '29']
    assert [c.code for c in sut.colors] == ['BLK', 'WHT', 'RED', 'PGR', 'CBT']


def test_filtered_valid():
    sut = create_sut(["White", "Cobalt"])

    assert [c.id for c in sut.colors] == ['02', '29']
    assert [c.code for c in sut.colors] == ['WHT', 'CBT']


def test_filtered_unknown():
    with pytest.raises(ValueError):
        create_sut(["White", "Roomba"])


def test_filtered_empty():
    sut = create_sut([])
    assert len(sut.colors) == 5


def test_color_from_code():
    sut = create_sut()

    assert sut.color_from_code('RED').name == 'Red'
    assert sut.color_from_code('YEL') is None


@pytest.mark.parametrize('hex, expected_code', closest_color_rgb_cases)
def test_closest_color_rgb(hex, expected_code):
    sut = create_sut()
    rgb = hex_to_rgb(hex)
    color = sut.closest_color(rgb[0], rgb[1], rgb[2])

    assert color.code == expected_code


def test_closest_color_multiple_lookups():
    sut = create_sut()
    c1 = sut.closest_color(0, 0, 0)
    c2 = sut.closest_color(0, 0, 0)

    assert c1 == c2


def test_closest_color_transparent():
    sut = create_sut()
    c1 = sut.closest_color(0, 0, 0, 0)

    assert c1 is None


def create_sut(name_whitelist=None):
    black = Color('16', 'BLK', 'Black', '#343234', '#343234', '#343234')
    white = Color('02', 'WHT', 'White', '#f7f7f2', '#f7f7f2', '#f7f7f2')
    red = Color('42', 'RED', 'Red', '#c43a44', '#c43a44', '#c43a44')
    green = Color('17', 'PGR', 'Parrot Green', '#00968a', '#00968a', '#00968a')
    blue = Color('29', 'CBT', 'Cobalt', '#0066b3', '#0066b3', '#0066b3')
    return Palette([black, white, red, green, blue], name_whitelist)


def create_pseudo_file(raw_txt):
    f = StringIO()
    f.write(raw_txt)
    f.seek(0)

    return f


def hex_to_rgb(hex):
    return tuple(int(hex[i:i + 2], 16) for i in (1, 3, 5))
