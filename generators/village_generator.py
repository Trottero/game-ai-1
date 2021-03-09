from generators.generator import Generator
import numpy as np
from blocks import Blocks


class VillageGenerator(Generator):
    """ Adds villages onto the map.

    ``probability`` -- probability to attempt generation on a chunk basis (default 0.5)

    ``village_size`` -- n x n size of each individual village (default 2)

    ``attempts`` -- maximum number of attempts (default 10)
    """

    def __init__(self, probability=0.1, village_size=2, attempts=10):
        self.probability = probability
        self.village_size = village_size
        self.attempts = attempts
        self.chunk_size = 20

    def apply(self, world, height_map):
        for x in range(0, len(world), self.chunk_size):
            for y in range(0, len(world), self.chunk_size):
                self.generate_town(x, y, world)
        return world, height_map

    def generate_town(self, x, y, world):
        size = len(world)
        # roll chance for every chunk:
        if np.random.rand() < self.probability:
            # Attempt to spawn a village in the given portion
            for _ in range(self.attempts):
                # Get random loc in this chunk
                r = np.random.rand(2) * 20
                x1, y1 = r
                x1 = x + int(x1)
                y1 = y + int(y1)
                selection = world[x1:min(x1 + self.village_size + 1, size),
                                  y1:min(y1 + self.village_size + 1, size)]
                selection = selection - Blocks.GRASS
                # check if all blocks in selection are grass
                if np.count_nonzero(selection) == 0:
                    # Success! spawn village at this x, y
                    world[x1:min(x1 + self.village_size + 1, size),
                          y1:min(y1 + self.village_size + 1, size)] = Blocks.VILLAGE
                    break
