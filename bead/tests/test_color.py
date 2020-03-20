from bead import Color


def test_id():
    assert create_sut().id == '01'


def test_code():
    assert create_sut().code == 'BLK'


def test_name():
    assert create_sut().name == 'BlaCK'


def test_hex_value():
    assert create_sut().hex_value == '#1a2b3c'


def test_repr():
    val = create_sut().__repr__()
    exp = "Color(id='01', code='BLK', name='BlaCK', hex_value='#1a2b3c')"
    assert val == exp


def test_is_white():
    # Variant casing
    assert Color('01', 'WHT', 'White', '#f7f7f2').is_white() is True
    assert Color('01', 'wht', 'white', '#f7f7f2').is_white() is True

    # Wrong code
    assert Color('01', 'QUE', 'White', '#f7f7f2').is_white() is False


def create_sut():
    return Color('01', 'bLk', 'BlaCK', '#1a2B3c')
