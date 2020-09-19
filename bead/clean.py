import os


def clean_project(project, commit=False):
    transient_files = project.get_transient_files()
    for transient_file in transient_files:
        if commit:
            print(f'Deleting -- Path:{transient_file}')
            os.remove(transient_file)
        else:
            print(f'Would clean -- Path:{transient_file}')
