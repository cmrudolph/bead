from bead import Properties


Txt_Full = '{"width":1,"height":2,"quantize_colors":3,"colors":["A", "B"]}'
Txt_Minimal = '{"width":1,"height":2}'


def test_from_json_full():
    sut = Properties.from_json(Txt_Full)
    assert_full(sut)


def test_from_json_minimal():
    sut = Properties.from_json(Txt_Minimal)
    assert_minimal(sut)


def test_create_new_full():
    sut = Properties.create(1, 2, 3, ['A', 'B'])
    assert_full(sut)


def test_create_new_minimal():
    sut = Properties.create(1, 2)
    assert_minimal(sut)


def test_to_json_full():
    sut = Properties.create(1, 2, 3, ['A', 'B'])
    j = sut.to_json()
    round_tripped = Properties.from_json(j)
    assert_full(round_tripped)


def test_to_json_minimal():
    sut = Properties.create(1, 2)
    j = sut.to_json()
    round_tripped = Properties.from_json(j)
    assert_minimal(round_tripped)


def assert_full(sut):
    assert sut.width == 1
    assert sut.height == 2
    assert sut.quantize_colors == 3
    assert sut.colors == ('A', 'B')


def assert_minimal(sut):
    assert sut.width == 1
    assert sut.height == 2
    assert sut.quantize_colors == 0
    assert sut.colors == ()
