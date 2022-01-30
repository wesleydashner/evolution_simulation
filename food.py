from typing import Tuple

from entity import Entity
from mask_ids import ORGANISM_ID, FOOD_ID


class Food(Entity):
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = (0, 200, 0)) -> None:
        super().__init__(x, y, FOOD_ID, color)

    def collide(self, other: Entity) -> bool:
        if other.mask_id == ORGANISM_ID:
            return False

    def is_present(self) -> bool:
        return True
