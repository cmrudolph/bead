from bead import Project, generate_layout
import filecmp
import os
import pytest
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
BASELINES_DIR = os.path.join(DATA_DIR, 'baselines')


@pytest.mark.filterwarnings("ignore:.*np.* deprecated:DeprecationWarning")
def test_generate(tmpdir):
    source_dir = os.path.join(DATA_DIR, 'projects', 'test_generate1')
    shutil.copytree(source_dir, tmpdir.join('test_generate1'))

    project = Project(tmpdir, 'test_generate1')
    baseline_path = os.path.join(BASELINES_DIR, 'test_generate1_layout.txt')

    generate_layout(project)
    assert filecmp.cmp(baseline_path, project.layout_path) is True


# @pytest.mark.filterwarnings("ignore:.*np.* deprecated:DeprecationWarning")
# def test_generate_overwrite(tmpdir):
#     palette_path = os.path.join(DATA_DIR, 'test_generate.palette.txt')
#     image_path = os.path.join(DATA_DIR, 'test_generate.png')
#     baseline_path = os.path.join(DATA_DIR, 'test_generate.bead')

#     layout_path = str(tmpdir.join('test_generate.bead'))

#     with open(layout_path, 'w') as f:
#         f.write('asdf')

#     generate_layout(palette_path, image_path, layout_path, 2, 2)
#     assert filecmp.cmp(baseline_path, layout_path) is True
