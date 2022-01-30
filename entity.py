from typing import Tuple


class Entity:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        self.x: int = x
        self.y: int = y
        self.color: Tuple[int, int, int] = color
