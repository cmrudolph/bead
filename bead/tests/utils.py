from bead import Properties, Project
import os
import shutil


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def get_baseline_path(file_name):
    return os.path.join(DATA_DIR, 'baselines', file_name)


def get_input_path(file_name):
    return os.path.join(DATA_DIR, 'input', file_name)


def copy_input(file_name, dest_path):
    src_path = get_input_path(file_name)
    shutil.copyfile(src_path, dest_path)


def create_project_folder(root, name, width, height, quant=10, colors=None):
    proj_path = os.path.join(root, name)
    os.mkdir(proj_path)

    # Dynamically create a properties file - an essential component of ALL
    # project structures
    props = Properties.create(width, height, quant, colors)
    props_path = os.path.join(proj_path, 'properties.json')
    with open(props_path, 'w') as f:
        f.write(props.to_json())

    return proj_path


def create_project(root, name, width, height, quant=10, colors=None):
    proj_path = create_project_folder(root, name, width, height, quant, colors)
    return Project(proj_path)
