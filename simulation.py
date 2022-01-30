from random import random, shuffle
from typing import List, Tuple, Optional
from itertools import combinations

from renderer import Renderer
from organism import Organism
from direction import Direction
from food import Food
from entity import Entity


class Simulation:
    def __init__(self) -> None:
        self.habitat_width: int = 100
        self.entities: List[Entity] = []
        self.habitat: List[List[List[Entity]]] = self.get_empty_habitat()
        self.renderer: Renderer = Renderer(10, self.habitat_width)
        # TODO: there's a bug with spawning because food only has spawn probability
        # TODO: for each space not already occupied by an organism
        self.spawn_organisms()
        self.spawn_food()

    def run(self) -> None:
        while True:
            self.renderer.render(self.get_board_for_renderer())
            self.move_organisms()
            self.do_collisions()
            self.check_if_present()

    def kill_entity(self, entity: Entity, x: int, y: int):
        self.habitat[y][x].remove(entity)
        self.entities.remove(entity)

    def do_collision(self, a: Entity, b: Entity, x: int, y: int):
        a_survives, b_survives = a.collide(b), b.collide(a)
        if not a_survives:
            self.kill_entity(a, x, y)
        if not b_survives:
            self.kill_entity(b, x, y)

    def do_collisions(self):
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if len(self.habitat[y][x]) > 1:
                    for pair in combinations(self.habitat[y][x], 2):
                        self.do_collision(pair[0], pair[1], x, y)

    def check_if_present(self):
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                for entity in self.habitat[y][x]:
                    if not entity.is_present():
                        self.kill_entity(entity, x, y)

    def move_organism(self, organism: Organism, direction: Direction) -> None:
        if direction is not None:
            self.habitat[organism.y][organism.x].remove(organism)
            delta_x, delta_y = direction.value
            organism.x += delta_x
            organism.y += delta_y
            self.habitat[organism.y][organism.x].append(organism)

    def move_organisms(self) -> None:
        # shuffle organisms, so first organisms don't always have an advantage of getting a desirable spot
        shuffle(self.entities)
        for entity in self.entities:
            if isinstance(entity, Organism):
                move = entity.get_move(self.get_possible_directions(entity))
                self.move_organism(entity, move)

    def get_possible_directions(self, organism: Organism) -> List[Direction]:
        possible_directions = []
        for direction in Direction:
            delta_x, delta_y = direction.value
            if self.is_valid_space(organism.x + delta_x, organism.y + delta_y):
                possible_directions.append(direction)
        return possible_directions

    def is_valid_space(self, x, y) -> bool:
        # TODO: use mask id's here
        return 0 <= x < self.habitat_width and 0 <= y < self.habitat_width and not self.space_has_organism(x, y)

    def space_has_organism(self, x, y) -> bool:
        for entity in self.habitat[y][x]:
            if isinstance(entity, Organism):
                return True
        return False

    def get_empty_habitat(self) -> List[List[List]]:
        return [[[] for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]

    def get_organism(self, x: int, y: int) -> Organism:
        return Organism(x, y)

    def get_food(self, x: int, y: int) -> Food:
        return Food(x, y)

    def spawn_food(self) -> None:
        self.spawn_entities(0.5, self.get_food)

    def spawn_organisms(self) -> None:
        self.spawn_entities(0.01, self.get_organism)

    def spawn_entities(self, spawn_probability: float, get_entity_method) -> None:
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if self.habitat[y][x] == [] and random() < spawn_probability:
                    new_entity = get_entity_method(x, y)
                    self.habitat[y][x].append(new_entity)
                    self.entities.append(new_entity)

    def get_board_for_renderer(self, default_color: Tuple[int, int, int] = (0, 0, 0)) -> List[List[Tuple[int, int, int]]]:
        board = [[default_color for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if self.habitat[y][x] != []:
                    # TODO: mask id's act as z-position
                    if len(self.habitat[y][x]) > 1:
                        board[y][x] = (255, 255, 255)
                    else:
                        board[y][x] = self.habitat[y][x][0].color
        return board
