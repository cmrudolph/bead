from bead import BeadColor


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
    assert val == "BeadColor('01', 'BLK', 'BlaCK', '#1a2b3c')"


def test_is_white():
    # Variant casing
    assert BeadColor('01', 'WHT', 'White', '#f7f7f2').is_white() is True
    assert BeadColor('01', 'wht', 'white', '#f7f7f2').is_white() is True

    # Wrong code
    assert BeadColor('01', 'QUE', 'White', '#f7f7f2').is_white() is False


def create_sut():
    return BeadColor('01', 'bLk', 'BlaCK', '#1a2B3c')
