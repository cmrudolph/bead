from bead import Project, export_layout
import filecmp
import os
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
BASELINES_DIR = os.path.join(DATA_DIR, 'baselines')


def test_export(tmpdir):
    source_dir = os.path.join(DATA_DIR, 'projects', 'test_export1')
    shutil.copytree(source_dir, tmpdir.join('test_export1'))

    project = Project(tmpdir, 'test_export1')
    baseline_path = os.path.join(BASELINES_DIR, 'test_export1_final.png')

    export_layout(project)
    assert filecmp.cmp(baseline_path, project.final_path) is True


# def test_export_overwrite(tmpdir):
#     palette_path = os.path.join(DATA_DIR, 'test_export.palette.txt')
#     layout_path = os.path.join(DATA_DIR, 'test_export.bead')
#     baseline_path = os.path.join(DATA_DIR, 'test_export.png')

#     image_path = str(tmpdir.join('test_export.png'))

#     with open(image_path, 'w') as f:
#         f.write('asdf')

#     export_layout(palette_path, layout_path, image_path, 30)
#     assert filecmp.cmp(baseline_path, image_path) is True
