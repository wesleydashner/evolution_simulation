from typing import Tuple, Optional, List, Dict
from random import random, choice

from food import Food
from direction import Direction
from entity import Entity
import constants


class EvolvingOrganism(Entity):
    def __init__(self, x: int, y: int, max_sight_range: int = 1, color: Tuple[int, int, int] = (127, 127, 127)) -> None:
        super().__init__(x, y, constants.ORGANISM_ID, color)
        self.food_count: float = constants.START_FOOD
        self.age = 0
        self.max_age = constants.MAX_AGE
        self.max_sight_range = max_sight_range

    def get_no_move_probability(self) -> float:
        return self.age / self.max_age

    def get_move(self, possible_directions: List[Direction], sight: Dict[Direction, list]) -> Optional[Direction]:
        if possible_directions == [] or random() < self.get_no_move_probability():
            return None
        best_direction = None
        shortest_distance = float('inf')
        for direction, data in sight.items():
            distance = data[0]
            e_types = data[1]
            if distance <= self.max_sight_range and e_types is not None and Food in e_types and distance < shortest_distance and direction in possible_directions:
                shortest_distance = distance
                best_direction = direction
        if best_direction is not None:
            self.food_count -= constants.MOVE_COST
            return best_direction
        self.food_count -= constants.STILL_COST
        return None

    def collide(self, other: Entity) -> bool:
        if other.mask_id == constants.FOOD_ID:
            self.food_count += 1
        return True

    def is_present(self) -> bool:
        self.age += 1
        if self.age == self.max_age:
            return False
        return self.food_count > 0

    def clamp_color_value(self, initial_value: int) -> int:
        if initial_value < 0:
            return 0
        if initial_value > 255:
            return 255
        return initial_value

    def get_offspring(self, x: int, y: int) -> Optional['EvolvingOrganism']:
        if self.food_count > constants.REPRODUCTION_COST:
            self.food_count = constants.START_FOOD
            max_sight_range_delta = choice([-1, 1])
            new_max_sight_range = self.max_sight_range + max_sight_range_delta
            return EvolvingOrganism(x, y, max_sight_range=new_max_sight_range, color=(self.clamp_color_value(self.color[0] + choice([-10, 10])), self.clamp_color_value(self.color[1] + choice([-10, 10])), self.clamp_color_value(self.color[2] + choice([-10, 10]))))
        return None
