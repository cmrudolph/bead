from bead import Project
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_load_project():
    root = os.path.join(DATA_DIR, 'projects')
    sut = Project(root, 'test_project1')

    assert sut.name == 'test_project1'
    assert sut.properties.width == 29
    assert sut.palette.color_from_code('WHT').name == 'White'

    assert 'test_project1' in sut.orig_path
    assert 'original.png' in sut.orig_path

    assert 'test_project1' in sut.quantized_path
    assert 'quantized.png' in sut.quantized_path

    assert 'test_project1' in sut.partitioned_path
    assert 'partitioned.png' in sut.partitioned_path

    assert 'test_project1' in sut.layout_path
    assert 'layout.txt' in sut.layout_path

    assert 'test_project1' in sut.final_path
    assert 'final.png' in sut.final_path
