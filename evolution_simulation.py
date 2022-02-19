from random import random, shuffle, choice
from typing import List, Tuple, Dict
from itertools import combinations

from renderer import Renderer
from organisms.evolving_organism import EvolvingOrganism
from direction import Direction
from food import Food
from entity import Entity
import constants


class EvolutionSimulation:
    def __init__(self) -> None:
        # TODO: make it so I don't have to change two numbers here to change habitat width
        self.habitat_width: int = 200
        self.organism_types: List[type] = [EvolvingOrganism]
        self.entities: List[Entity] = []
        self.habitat: List[List[List[Entity]]] = self.get_empty_habitat()
        self.renderer: Renderer = Renderer(6, self.habitat_width)
        self.spawn_organisms()
        self.spawn_food()

    def run(self) -> None:
        while True:
            self.renderer.render(self.get_board_for_renderer())
            self.move_organisms()
            self.do_collisions()
            self.check_if_present()
            self.spawn_food(0.001)
            self.do_reproductions()
            total_speed = 0
            total_sight = 0
            total_red = 0
            total_green = 0
            total_blue = 0
            total_organisms = self.get_entity_type_count(EvolvingOrganism)
            for entity in self.entities:
                if isinstance(entity, EvolvingOrganism):
                    total_speed += entity.speed
                    total_sight += entity.sight
                    total_red += entity.color[0]
                    total_green += entity.color[1]
                    total_blue += entity.color[2]
            print(f'AVERAGE SPEED: {total_speed / total_organisms}')
            print(f'AVERAGE SIGHT: {total_sight / total_organisms}')
            print(f'AVERAGE RED: {total_red / total_organisms}')
            print(f'AVERAGE GREEN: {total_green / total_organisms}')
            print(f'AVERAGE BLUE: {total_blue / total_organisms}')
            print()

    def print_organism_counts(self):
        for o_type in self.organism_types:
            print(f'{o_type.__name__}: {self.get_entity_type_count(o_type)}')
        print()

    def get_entity_type_count(self, entity_type: type):
        count = 0
        for entity in self.entities:
            if isinstance(entity, entity_type):
                count += 1
        return count

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

    def do_reproductions(self):
        for entity in self.entities:
            if self.is_organism(entity):
                possible_directions = self.get_possible_directions(entity)
                if possible_directions != []:
                    delta_x, delta_y = choice(possible_directions).value
                    x = entity.x + delta_x
                    y = entity.y + delta_y
                    offspring = entity.get_offspring(x, y)
                    if offspring is not None:
                        self.spawn_entity(offspring, x, y)

    def check_if_present(self):
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                for entity in self.habitat[y][x]:
                    if not entity.is_present():
                        self.kill_entity(entity, x, y)

    def move_organism(self, organism: EvolvingOrganism, direction: Direction) -> None:
        organism.food_count -= constants.MOVE_COST
        if organism.food_count <= 0:
            return
        self.habitat[organism.y][organism.x].remove(organism)
        delta_x, delta_y = direction.value
        organism.x += delta_x
        organism.y += delta_y
        self.habitat[organism.y][organism.x].append(organism)

    def move_organisms(self) -> None:
        # shuffle organisms, so first organisms don't always have an advantage of getting a desirable spot
        shuffle(self.entities)
        for entity in self.entities:
            if self.is_organism(entity):
                moves = entity.get_moves(self.get_sight(entity))
                for move in moves:
                    delta_x, delta_y = move.value
                    new_x = entity.x + delta_x
                    new_y = entity.y + delta_y
                    if self.is_valid_space(new_x, new_y, entity):
                        self.move_organism(entity, move)
                    else:
                        break

    def get_sight(self, entity: Entity) -> Dict[Direction, list]:
        return_dict = {}
        for direction in Direction:
            return_dict[direction] = self.get_sight_in_direction(entity, direction)
        return return_dict

    def get_sight_in_direction(self, entity: Entity, direction: Direction) -> list:
        count = 0
        x = entity.x
        y = entity.y
        while True:
            count += 1
            delta_x, delta_y = direction.value
            x += delta_x
            y += delta_y
            if not 0 <= x < self.habitat_width or not 0 <= y < self.habitat_width:
                return [count, None]
            if self.habitat[y][x] != []:
                return [count, self.get_visible_entity(x, y).color]

    def get_possible_directions(self, organism: EvolvingOrganism) -> List[Direction]:
        possible_directions = []
        for direction in Direction:
            delta_x, delta_y = direction.value
            if self.is_valid_space(organism.x + delta_x, organism.y + delta_y, organism):
                possible_directions.append(direction)
        return possible_directions

    def is_valid_space(self, x: int, y: int, organism: EvolvingOrganism) -> bool:
        if not 0 <= x < self.habitat_width or not 0 <= y < self.habitat_width:
            return False
        for entity in self.habitat[y][x]:
            if entity.mask_id == organism.mask_id:
                return False
        return True

    def get_empty_habitat(self) -> List[List[List]]:
        return [[[] for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]

    def get_organism(self, x: int, y: int) -> EvolvingOrganism:
        chosen_type = choice(self.organism_types)
        return chosen_type(x, y)

    def is_organism(self, entity: Entity) -> bool:
        return any([isinstance(entity, o_type) for o_type in self.organism_types])

    def get_food(self, x: int, y: int) -> Food:
        return Food(x, y)

    def spawn_food(self, spawn_probability: float = 0.5) -> None:
        self.spawn_entities(spawn_probability, self.get_food)

    def spawn_organisms(self) -> None:
        self.spawn_entities(0.005, self.get_organism)

    def spawn_entity(self, entity: Entity, x: int, y: int) -> None:
        self.habitat[y][x].append(entity)
        self.entities.append(entity)

    def spawn_entities(self, spawn_probability: float, get_entity_method) -> None:
        adjusted_spawn_probability = self.get_adjusted_spawn_probability(spawn_probability)
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if self.habitat[y][x] == [] and random() < adjusted_spawn_probability:
                    new_entity = get_entity_method(x, y)
                    self.spawn_entity(new_entity, x, y)

    # this method adjusts spawn probability based on how many entities there already. for example, if there are 4
    # spaces, and 2 of these contain organisms, and we want food to have a 0.5 spawn probability then the actual
    # spawn probability needs to be 1. NOTE: this method assumes that each entity occupies exactly one space and that
    # two entities cannot occupy the same space
    def get_adjusted_spawn_probability(self, spawn_probability: float):
        entity_count = len(self.entities)
        total_spaces = self.habitat_width ** 2
        spaces_available = total_spaces - entity_count
        if spaces_available == 0:
            return 0
        ratio = total_spaces / spaces_available
        return min(spawn_probability * ratio, 1)

    def get_visible_entity(self, x: int, y: int) -> Entity:
        return max(self.habitat[y][x], key=lambda e: e.mask_id)

    def get_board_for_renderer(self, default_color: Tuple[int, int, int] = (0, 0, 0)) -> List[List[Tuple[int, int, int]]]:
        board = [[default_color for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]
        for y in range(self.habitat_width):
            for x in range(self.habitat_width):
                if self.habitat[y][x] != []:
                    board[y][x] = self.get_visible_entity(x, y).color
        return board
