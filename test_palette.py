from palette import BeadPalette, BeadColor


def test_colors():
    c1 = BeadColor('01', 'C1', '#aaaaaa')
    c2 = BeadColor('02', 'C2', '#bbbbbb')
    sut = BeadPalette([c1, c2])

    assert sut.colors == [c1, c2]


def test_from_txt():
    raw = '16  |  Black                |  #343234\n39  |  Dark Gray            |  #56575c'
    sut = BeadPalette.from_txt(raw)

    assert [c.id for c in sut.colors] == ['16', '39']
    assert [c.name for c in sut.colors] == ['Black', 'Dark Gray']
    assert [c.hex_value for c in sut.colors] == ['#343234', '#56575c']


def test_id_from_hex_value():
    raw = '16  |  Black                |  #343234\n39  |  Dark Gray            |  #56575c'
    sut = BeadPalette.from_txt(raw)

    assert sut.id_from_hex_value('#343234') == '16'
    assert sut.id_from_hex_value('#123123') == None


def test_hex_value_from_id():
    raw = '16  |  Black                |  #343234\n39  |  Dark Gray            |  #56575c'
    sut = BeadPalette.from_txt(raw)

    assert sut.hex_value_from_id('16') == '#343234'
    assert sut.hex_value_from_id('888') == None
