import fire
from bead import export_layout


class Cli():
    def export(self, palette_path, layout_path, output_path, cell_size):
        export_layout(palette_path, layout_path, output_path, cell_size)


if __name__ == "__main__":
    fire.Fire(Cli)
