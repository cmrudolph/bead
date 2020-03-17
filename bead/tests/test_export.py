from bead import export_layout
import filecmp
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_export(tmpdir):
    palette_path = os.path.join(DATA_DIR, 'test_export.palette.txt')
    layout_path = os.path.join(DATA_DIR, 'test_export.bead')
    baseline_path = os.path.join(DATA_DIR, 'test_export.png')
    output_path = str(tmpdir.join('test_export.png'))

    export_layout(palette_path, layout_path, output_path, 30)
    assert filecmp.cmp(baseline_path, output_path) is True


def test_export_overwrite(tmpdir):
    palette_path = os.path.join(DATA_DIR, 'test_export.palette.txt')
    layout_path = os.path.join(DATA_DIR, 'test_export.bead')
    baseline_path = os.path.join(DATA_DIR, 'test_export.png')
    output_path = str(tmpdir.join('test_export.png'))

    with open(output_path, 'w') as f:
        f.write('asdf')

    export_layout(palette_path, layout_path, output_path, 30)
    assert filecmp.cmp(baseline_path, output_path) is True
