from palette import BeadPalette


def test_colors():
    sut = BeadPalette(['#aaaaaa', '#bbbbbb'])

    assert sut.colors == ['#aaaaaa', '#bbbbbb']


def test_has_color():
    sut = BeadPalette(['#aaaaaa'])

    assert sut.has_color('#aaaaaa') is True
    assert sut.has_color('#bbbbbb') is False


def test_from_json():
    raw = (
        '{"colors":[{"code":"#aaaaaa","comment":"C1"},{"code":"#bbbbbb"'
        ',"comment": "C2"}]}')
    sut = BeadPalette.from_json(raw)

    assert sut.colors == ['#aaaaaa', '#bbbbbb']
