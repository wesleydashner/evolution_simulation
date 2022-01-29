from enum import Enum


class Direction(Enum):
    # value is delta_x, delta_y for that direction
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
