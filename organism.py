from typing import Tuple
from direction import Direction
from random import choice, randint


class Organism:
    def __init__(self, x: int, y: int, habitat_width: int, color: Tuple[int, int, int] = (255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.habitat_width = habitat_width

    def move(self, direction: Direction):
        delta_x = direction.value[0]
        delta_y = direction.value[1]
        new_x = self.x + delta_x
        new_y = self.y + delta_y
        if 0 < new_x < self.habitat_width and 0 < new_y < self.habitat_width:
            self.x = new_x
            self.y = new_y

    def random_move(self):
        self.move(choice(list(Direction)))
