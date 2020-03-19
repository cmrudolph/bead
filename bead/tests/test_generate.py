from bead import generate_layout
import filecmp
import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@pytest.mark.filterwarnings("ignore:.*np.* deprecated:DeprecationWarning")
def test_generate(tmpdir):
    palette_path = os.path.join(DATA_DIR, 'test_generate.palette.txt')
    image_path = os.path.join(DATA_DIR, 'test_generate.png')
    baseline_path = os.path.join(DATA_DIR, 'test_generate.bead')

    layout_path = str(tmpdir.join('test_generate.bead'))

    generate_layout(palette_path, image_path, layout_path, 2, 2)
    assert filecmp.cmp(baseline_path, layout_path) is True


@pytest.mark.filterwarnings("ignore:.*np.* deprecated:DeprecationWarning")
def test_generate_overwrite(tmpdir):
    palette_path = os.path.join(DATA_DIR, 'test_generate.palette.txt')
    image_path = os.path.join(DATA_DIR, 'test_generate.png')
    baseline_path = os.path.join(DATA_DIR, 'test_generate.bead')

    layout_path = str(tmpdir.join('test_generate.bead'))

    with open(layout_path, 'w') as f:
        f.write('asdf')

    generate_layout(palette_path, image_path, layout_path, 2, 2)
    assert filecmp.cmp(baseline_path, layout_path) is True
