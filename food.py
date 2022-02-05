from typing import Tuple

from entity import Entity
import constants


class Food(Entity):
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = constants.GREEN) -> None:
        super().__init__(x, y, constants.FOOD_ID, color)

    def collide(self, other: Entity) -> bool:
        if other.mask_id == constants.ORGANISM_ID:
            return False

    def is_present(self) -> bool:
        return True
