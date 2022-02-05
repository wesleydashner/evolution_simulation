from typing import Tuple, Optional, List, Dict
from random import choice, random

from direction import Direction
from entity import Entity
import constants


class RandomOrganism(Entity):
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = constants.BLUE) -> None:
        super().__init__(x, y, constants.ORGANISM_ID, color)
        self.food_count: float = constants.START_FOOD
        self.age = 0
        self.max_age = constants.MAX_AGE

    def get_no_move_probability(self) -> float:
        return self.age / self.max_age

    def get_move(self, possible_directions: List[Direction], sight: Dict[Direction, list]) -> Optional[Direction]:
        if possible_directions == [] or random() < self.get_no_move_probability():
            self.food_count -= constants.STILL_COST
            return None
        self.food_count -= constants.MOVE_COST
        return choice(possible_directions)

    def collide(self, other: Entity) -> bool:
        if other.mask_id == constants.FOOD_ID:
            self.food_count += 1
        return True

    def is_present(self) -> bool:
        self.age += 1
        if self.age == self.max_age:
            return False
        return self.food_count > 0

    def should_reproduce(self) -> bool:
        if self.food_count > constants.REPRODUCTION_COST:
            self.food_count = constants.START_FOOD
            return True
        return False
