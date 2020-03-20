import pytest
from bead import Palette, Color
from io import StringIO


comparison_cases = [
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
    raw = ('02  |  RED  |  Radical Red  |  #a1B2c3\n\n'
           '01  |  BLU  |  Beautiful Blue  |  #F9e8D7\n\n')
    sut = Palette.create_from_txt(raw)

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Radical Red', 'Beautiful Blue']
    assert [c.hex_value for c in sut.colors] == ['#a1b2c3', '#f9e8d7']


def test_create_from_file():
    raw = ('02  |  RED  |  Radical Red  |  #a1B2c3\n\n'
           '01  |  BLU  |  Beautiful Blue  |  #F9e8D7\n\n')
    f = create_pseudo_file(raw)
    sut = Palette.create_from_file(f)

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Radical Red', 'Beautiful Blue']
    assert [c.hex_value for c in sut.colors] == ['#a1b2c3', '#f9e8d7']


def test_construct_directly():
    sut = create_sut()

    assert [c.id for c in sut.colors] == ['16', '02', '42', '17', '29']
    assert [c.code for c in sut.colors] == ['BLK', 'WHT', 'RED', 'PGR', 'CBT']


def test_code_from_hex_value():
    sut = create_sut()

    assert sut.color_from_hex_value('#c43a44').code == 'RED'
    assert sut.color_from_hex_value('#C43A44').code == 'RED'
    assert sut.color_from_hex_value('#ffffff') is None


def test_hex_value_from_code():
    sut = create_sut()

    assert sut.color_from_code('RED').hex_value == '#c43a44'
    assert sut.color_from_code('YEL') is None


@pytest.mark.parametrize('hex, expected_code', comparison_cases)
def test_closest_color(hex, expected_code):
    sut = create_sut()
    rgb = hex_to_rgb(hex)
    color = sut.closest_color(rgb[0], rgb[1], rgb[2])

    assert color.code == expected_code


def create_sut():
    black = Color('16', 'BLK', 'Black', '#343234')
    white = Color('02', 'WHT', 'White', '#f7f7f2')
    red = Color('42', 'RED', 'Red', '#c43a44')
    green = Color('17', 'PGR', 'Parrot Green', '#00968a')
    blue = Color('29', 'CBT', 'Cobalt', '#0066b3')
    return Palette([black, white, red, green, blue])


def create_pseudo_file(raw_txt):
    f = StringIO()
    f.write(raw_txt)
    f.seek(0)

    return f


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
