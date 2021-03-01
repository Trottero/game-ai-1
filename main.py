from generators.land_generator import LandGenerator
from world import World


if __name__ == '__main__':
    w = World()
    w.generate([LandGenerator()])
    w.export_to_fig()
