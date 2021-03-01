import numpy as np
from matplotlib import pyplot as plt
from typing import List
from generators.generator import Generator


class World():
    pallete = {
        # Grass
        1: [0, 128, 0],
        # Water
        2: [0, 0, 128]
    }

    def __init__(self, size=50):
        self.world = np.ones((50, 50))
        pass

    def generate(self, generators: List[Generator]):
        # apply all of the modifications that the world generators make.
        for generator in generators:
            self.world = generator.apply(self.world)
            pass

    def export_to_fig(self, filename='world'):
        # convert to (size, size, rgb)
        flattened = self.world.flatten()
        colored = np.array([World._color_convert(f) for f in flattened])
        colored = colored.reshape(50, 50, 3)

        plt.imsave(f'{filename}.png', colored)
        plt.show()
        pass

    def _color_convert(element):
        return np.array(World.pallete[element], dtype=np.uint8)
