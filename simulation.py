from random import random, shuffle
from typing import List, Tuple, Optional

from renderer import Renderer
from organism import Organism
from direction import Direction


class Simulation:
    def __init__(self):
        self.habitat_width: int = 200
        self.organisms: List[Organism] = []
        self.habitat: List[List[Optional[Organism]]] = self.get_empty_habitat()
        self.renderer: Renderer = Renderer(5, self.habitat_width)
        self.spawn_organisms()

    def run(self):
        while True:
            self.renderer.render(self.get_board_for_renderer())
            self.move_organisms()
            print(len(self.organisms))

    def move_organism(self, organism: Organism, direction: Direction):
        if direction is not None:
            self.habitat[organism.y][organism.x] = None
            delta_x, delta_y = direction.value
            organism.x += delta_x
            organism.y += delta_y
            self.habitat[organism.y][organism.x] = organism

    def move_organisms(self):
        # shuffle organisms, so first organisms don't always have an advantage of getting a desirable spot
        shuffle(self.organisms)
        for organism in self.organisms:
            move = organism.get_random_move(self.get_possible_directions(organism))
            self.move_organism(organism, move)

    def get_possible_directions(self, organism: Organism):
        possible_directions = []
        for direction in Direction:
            delta_x, delta_y = direction.value
            if self.is_empty(organism.x + delta_x, organism.y + delta_y):
                possible_directions.append(direction)
        return possible_directions

    def is_empty(self, x, y):
        return 0 <= x < self.habitat_width and 0 <= y < self.habitat_width and self.habitat[y][x] is None

    def get_empty_habitat(self):
        return [[None for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]

    def get_organism(self, x: int, y: int):
        return Organism(x, y)

    def spawn_organisms(self, spawn_probability: float = 0.01):
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if random() < spawn_probability:
                    new_organism = self.get_organism(x, y)
                    self.habitat[y][x] = new_organism
                    self.organisms.append(new_organism)

    def get_board_for_renderer(self, default_color: Tuple[int, int, int] = (0, 0, 0)):
        board = [[default_color for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if self.habitat[y][x] is not None:
                    board[y][x] = self.habitat[y][x].color
        return board
