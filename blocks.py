class Blocks():
    GRASS = 1
    WOODS = 2
    WATER = 3
    OCEAN = 4
    SAND = 5
    VILLAGE = 6
    PATH = 7
    WATER_PATH = 8
    pallete = {
        # Grass
        1: [148, 186, 101],
        2: [105, 139, 60],

        # Water
        3: [39, 144, 176],
        4: [43, 78, 114],

        # Sand
        5: [194, 178, 128],

        # village
        6: [132, 71, 40],
        # path
        7: [184, 115, 66],
        # Water path
        8: [118, 128, 116]
    }

    def __init__(self):
        pass
