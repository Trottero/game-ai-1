import numpy as np
from generators.generator import Generator


class LandGenerator(Generator):
    def __init__(self):
        pass

    def apply(self, world):
        world[10:20, 10:20] = np.ones((10, 10)) * 2
        return world
        pass
