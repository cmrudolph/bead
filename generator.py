import fire
from bead import generate_layout


class Cli():
    def generate(self, palette_path, image_path, output_path, width, height):
        export_layout(palette_path, layout_path, output_path, width, height)


if __name__ == "__main__":
    fire.Fire(Cli)
