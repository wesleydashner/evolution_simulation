from typing import Tuple, Optional, List
from random import choice

from direction import Direction
from entity import Entity


class Organism(Entity):
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        super().__init__(x, y, color)

    def get_move(self, possible_directions: List[Direction]) -> Optional[Direction]:
        if possible_directions == []:
            return None
        return choice(possible_directions)
