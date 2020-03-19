import fire
from bead import generate_layout


class Cli():
    def generate(self, palette_path, image_path, layout_path, width, height):
        generate_layout(palette_path, image_path, layout_path, width, height)


if __name__ == "__main__":
    fire.Fire(Cli)
