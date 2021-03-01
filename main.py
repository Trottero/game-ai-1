from generators.road_generator import RoadGenerator
from generators.village_generator import VillageGenerator
from generators.beach_generator import BeachGenerator
from generators.land_generator import LandGenerator
from world import World


if __name__ == '__main__':
    w = World(128)
    w.generate([LandGenerator(), BeachGenerator(),
                VillageGenerator(), RoadGenerator()])
    w.export_to_fig()
