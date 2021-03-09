from blocks import Blocks
import numpy as np
from matplotlib import pyplot as plt
from typing import List
from generators.generator import Generator
import os


class World():

    def __init__(self, size=50, seed=1337):
        self.rng = np.random.default_rng(int(seed, base=36))
        self.world = self.rng.random((size, size))
        self.height_map = self.rng.random((size, size))
        self.seed = seed
        self.size = size
        pass

    def generate(self, generators: List[Generator]):
        # apply all of the modifications that the world generators make.
        for generator in generators:
            self.world, self.height_map = generator.apply(
                self.world, self.height_map)
            pass

    def export_to_fig(self, filename='world'):
        # convert to (size, size, rgb)
        os.makedirs('worlds', exist_ok=True)
        plt.imsave(
            f'worlds/{self.seed}_{filename}_height.png', self.height_map)

        flattened = self.world.flatten()
        colored = np.array([World._color_convert(f) for f in flattened])
        colored = colored.reshape(self.size, self.size, 3)
        plt.imsave(f'worlds/{self.seed}_{filename}.png', colored)
        plt.show()
        pass

    def _color_convert(element):
        return np.array(Blocks.pallete[element], dtype=np.uint8)
