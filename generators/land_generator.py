from blocks import Blocks
import numpy as np
from math import cos, sin
from generators.generator import Generator
import scipy as sp
import scipy.ndimage


class LandGenerator(Generator):
    def __init__(self):
        pass

    def apply(self, world, height_map):
        for x in range(len(world)):
            for y in range(len(world)):
                world[x, y] = self.perlin(x, y)
        # world = np.array(world) + world.min()
        # world = world / np.max(world)
        world = sp.ndimage.filters.gaussian_filter(
            world, [5.0, 5.0], mode='constant')

        difference = float(world.max() - world.min())
        height_map = (world - world.min()) / difference
        v = np.vectorize(self.block_picker)
        return v(height_map), height_map

    # Use Perlin noise generation
    def interpolate(self, a0, a1, w):
        return(a1 - a0) * w + a0

    def random_gradient(self, ix, iy):
        random = 2920.0 * sin(ix * 21942.0 + iy * 171324.0 + 8912.0) * \
            cos(ix * 23157.0 * iy * 217832.0 + 9758.0)
        return (cos(random), sin(random))

    def dot_grid_gradient(self, ix, iy, x, y):
        gradx, grady = self.random_gradient(ix, iy)

        dx = x - ix
        dy = y - iy

        return dx*gradx + dy * grady

    def perlin(self, x, y):
        x0 = x
        x1 = x + 1
        y0 = y
        y1 = y + 1

        sx = -0.1
        sy = -0.1

        n0 = self.dot_grid_gradient(x0, y0, x, y)
        n1 = self.dot_grid_gradient(x1, y0, x, y)
        ix0 = self.interpolate(n0, n1, sx)

        n0 = self.dot_grid_gradient(x0, y1, x, y)
        n1 = self.dot_grid_gradient(x1, y1, x, y)
        ix1 = self.interpolate(n0, n1, sx)

        return self.interpolate(ix0, ix1, sy)

    def block_picker(self, val):
        # Woods
        if val > 0.8:
            return Blocks.WOODS
        # Plains
        if val > 0.5:
            return Blocks.GRASS
        # deep ocean
        if val < 0.3:
            return Blocks.OCEAN
        return Blocks.WATER
