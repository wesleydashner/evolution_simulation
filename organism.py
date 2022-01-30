from typing import Tuple
from random import choice


class Organism:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = (255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color

    def get_random_move(self, possible_directions):
        if possible_directions == []:
            return None
        return choice(possible_directions)
