from palette import BeadPalette, BeadColor


def test_colors():
    c1 = BeadColor('C1', '#aaaaaa')
    c2 = BeadColor('C2', '#bbbbbb')
    sut = BeadPalette([c1, c2])

    assert sut.colors == [c1, c2]


def test_has_color():
    c1 = BeadColor('C1', '#aaaaaa')
    sut = BeadPalette([c1])

    assert sut.has_color('#aaaaaa') is True
    assert sut.has_color('#bbbbbb') is False


def test_from_json():
    raw = (
        '{"colors":[{"value":"#aaaaaa","name":"C1"},{"value":"#bbbbbb"'
        ',"name": "C2"}]}')
    sut = BeadPalette.from_json(raw)

    c1 = BeadColor('C1', '#aaaaaa')
    c2 = BeadColor('C2', '#bbbbbb')
    assert [c.value for c in sut.colors] == ['#aaaaaa', '#bbbbbb']
