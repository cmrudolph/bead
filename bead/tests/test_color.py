from bead import Color


def test_id():
    assert create_sut().id == '01'


def test_code():
    assert create_sut().code == 'BLK'


def test_name():
    assert create_sut().name == 'BlaCK'


def test_hex_internal():
    assert create_sut().hex_internal == '#a1111a'


def test_hex_view():
    assert create_sut().hex_view == '#b2222b'


def test_hex_edge():
    assert create_sut().hex_edge == '#c3333c'


def test_repr():
    val = create_sut().__repr__()
    exp = ("Color(id='01', code='BLK', name='BlaCK', hex_internal='#a1111a', "
           "hex_view='#b2222b', hex_edge='#c3333c')")
    assert val == exp


def create_sut():
    return Color('01', 'bLk', 'BlaCK', '#a1111A', '#b2222B', '#c3333C')
