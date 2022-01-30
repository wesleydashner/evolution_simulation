from typing import Tuple
from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, x: int, y: int, mask_id: int, color: Tuple[int, int, int]) -> None:
        self.x: int = x
        self.y: int = y
        self.mask_id = mask_id
        self.color: Tuple[int, int, int] = color

    # returns true if entity should remain in habitat, false if it should be removed
    @abstractmethod
    def collide(self, other: 'Entity') -> bool:
        pass

    # returns false if entity should be removed, true otherwise
    # gets called before each frame
    @abstractmethod
    def is_present(self) -> bool:
        pass
