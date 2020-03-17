from bead import BeadPalette, BeadColor
from io import StringIO


def test_load_from_txt():
    raw = ('02  |  RED  |  Radical Red  |  #a1B2c3\n\n'
           '01  |  BLU  |  Beautiful Blue  |  #F9e8D7\n\n')
    sut = BeadPalette.load_from_txt(raw)

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Radical Red', 'Beautiful Blue']
    assert [c.hex_value for c in sut.colors] == ['#a1b2c3', '#f9e8d7']


def test_load_from_file():
    raw = ('02  |  RED  |  Radical Red  |  #a1B2c3\n\n'
           '01  |  BLU  |  Beautiful Blue  |  #F9e8D7\n\n')
    f = create_pseudo_file(raw)
    sut = BeadPalette.load_from_file(f)

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Radical Red', 'Beautiful Blue']
    assert [c.hex_value for c in sut.colors] == ['#a1b2c3', '#f9e8d7']


def test_construct_directly():
    sut = create_sut()

    assert [c.id for c in sut.colors] == ['02', '01']
    assert [c.code for c in sut.colors] == ['RED', 'BLU']
    assert [c.name for c in sut.colors] == ['Radical Red', 'Beautiful Blue']
    assert [c.hex_value for c in sut.colors] == ['#a1b2c3', '#f9e8d7']


def test_code_from_hex_value():
    sut = create_sut()

    assert sut.color_from_hex_value('#a1B2c3').code == 'RED'
    assert sut.color_from_hex_value('#A1B2C3').code == 'RED'
    assert sut.color_from_hex_value('#ffffff') is None


def test_hex_value_from_code():
    sut = create_sut()

    assert sut.color_from_code('RED').hex_value == '#a1b2c3'
    assert sut.color_from_code('YEL') is None


def create_sut():
    c1 = BeadColor('02', 'RED', 'Radical Red', '#a1B2c3')
    c2 = BeadColor('01', 'BLU', 'Beautiful Blue', '#F9e8D7')
    return BeadPalette([c1, c2])


def create_pseudo_file(raw_txt):
    f = StringIO()
    f.write(raw_txt)
    f.seek(0)

    return f
