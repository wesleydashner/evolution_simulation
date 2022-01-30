from typing import Tuple, Optional, List
from random import choice

from direction import Direction
from entity import Entity
from mask_ids import ORGANISM_ID, FOOD_ID


class Organism(Entity):
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        super().__init__(x, y, ORGANISM_ID, color)
        self.food_count: float = 5

    def get_move(self, possible_directions: List[Direction]) -> Optional[Direction]:
        if possible_directions == []:
            return None
        return choice(possible_directions)

    def collide(self, other: Entity) -> bool:
        if other.mask_id == FOOD_ID:
            self.food_count += 1
        return True

    def is_present(self) -> bool:
        self.food_count -= 0.1
        return self.food_count > 0

    def should_reproduce(self) -> bool:
        if self.food_count > 15:
            self.food_count = 5
            return True
        return False
