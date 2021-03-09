from generators import road_generator
from generators.road_generator import RoadGenerator
from generators.village_generator import VillageGenerator
from generators.beach_generator import BeachGenerator
from generators.land_generator import LandGenerator
from world import World


if __name__ == '__main__':
    fruits = ['banana', 'dragonfruit', 'grapefruit',
              'blueberry', 'watermelon', 'papaya']

    for fruit in fruits:
        w = World(100, seed=fruit)
        w.generate([LandGenerator(apply_gaussian=True, apply_perlin=True, rng=w.rng), BeachGenerator(),
                    VillageGenerator(rng=w.rng), RoadGenerator()])
        w.export_to_fig(type='pdf')
