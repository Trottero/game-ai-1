from generators.generator import Generator
import numpy as np
from blocks import Blocks


class BeachGenerator(Generator):

    def __init__(self, kernel_size=1, n_water=1, n_grass=2):
        # Kernel_size determines the width of the beach
        self.kernel_size = kernel_size
        self.n_water = n_water
        self.n_grass = n_grass
        pass

    def apply(self, world, height_map):
        size = len(world)
        for x in range(size):
            for y in range(size):
                world[x, y] = self.apply_kernel(world, x, y, size)
        return world, height_map

    def apply_kernel(self, world, x, y, size):
        # Gets kernel selection
        selection = world[max(x - self.kernel_size, 0):
                          min(x + self.kernel_size + 1, size),
                          max(y - self.kernel_size, 0):
                          min(y + self.kernel_size + 1, size)]

        unique, counts = np.unique(selection, return_counts=True)
        c = dict(zip(unique, counts))
        # Check the selection for the required numbers
        if Blocks.WATER in c.keys() and Blocks.GRASS in c.keys() and world[x, y] == Blocks.GRASS:
            if Blocks.SAND in c.keys():
                c[Blocks.GRASS] += c[Blocks.SAND]
            if c[Blocks.WATER] >= self.n_water and c[Blocks.GRASS] >= self.n_grass:
                return Blocks.SAND
        return world[x, y]
