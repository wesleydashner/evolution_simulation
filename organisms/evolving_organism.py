from typing import Tuple, Optional, List, Dict
from random import random, choice, shuffle
from math import sqrt

from direction import Direction
from entity import Entity
import constants


class EvolvingOrganism(Entity):
    def __init__(self, x: int, y: int, sight: int = 1, speed: int = 1, size: int = 1, is_aggressive: bool = False,
                 color: Tuple[int, int, int] = (127, 127, 127)) -> None:
        super().__init__(x, y, constants.ORGANISM_ID, color)
        self.food_count: float = constants.START_FOOD
        self.age = 0
        self.max_age = constants.MAX_AGE
        self.sight = sight
        self.speed = speed
        self.size = size
        self.is_aggressive = is_aggressive

    def get_no_move_probability(self) -> float:
        return self.age / self.max_age

    def get_moves(self, sight: Dict[Direction, list]) -> List[Direction]:
        self.food_count -= constants.COST_TO_LIVE * self.sight
        self.food_count -= constants.COST_TO_LIVE * self.size
        if random() < self.get_no_move_probability():
            return []
        best_direction, best_score, shortest_distance = self.__get_best_direction_and_score(sight)
        if best_direction is not None:
            return [best_direction] * min(self.speed, shortest_distance)
        return []

    def __get_best_direction_and_score(self, sight: Dict[Direction, list]) -> Tuple[Direction, int, int]:
        best_direction = None
        best_score = 0
        shortest_distance = float('inf')
        items = list(sight.items())
        shuffle(items)
        for direction, data in items:
            distance = data[0]
            color = data[1]
            score = self.__get_score(distance, color)
            if distance <= self.sight and score > best_score:
                best_score = score
                best_direction = direction
            if distance < shortest_distance:
                shortest_distance = distance
        return best_direction, best_score, shortest_distance

    def __get_score(self, distance: int, color: Tuple[int, int, int]) -> float:
        if color is None:
            return 0
        red1, green1, blue1 = color
        red2, green2, blue2 = constants.GREEN
        color_distance = sqrt((red1 - red2) ** 2 + (green1 - green2) ** 2 + (blue1 - blue2) ** 2)
        color_score = (color_distance / sqrt((255 ** 2) * 3))
        if not self.is_aggressive:
            color_score = color_score * -1 + 1
        if distance > self.sight:
            distance_score = 0
        else:
            distance_score = ((distance - 1) / (self.sight - 1 if self.sight > 1 else 1) * -1) + 1
        score = color_score + distance_score
        return score

    def collide(self, other: Entity) -> bool:
        if other.mask_id == constants.FOOD_ID:
            self.food_count += 1
        if other.mask_id == constants.ORGANISM_ID:
            if other.size > self.size:
                return False
            elif other.size < self.size:
                self.food_count += other.food_count
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

    def __get_offspring(self, x: int, y: int) -> Optional['EvolvingOrganism']:
        return EvolvingOrganism(x, y, sight=max(self.sight + choice([-1, 1]), 0), speed=max(self.speed + choice([-1, 1]), 0), size=max(self.size + choice([-1, 1]), 1), is_aggressive=self.is_aggressive if random() < 0.9 else not self.is_aggressive, color=(
            self.clamp_color_value(self.color[0] + choice([-10, 10])),
            self.clamp_color_value(self.color[1] + choice([-10, 10])),
            self.clamp_color_value(self.color[2] + choice([-10, 10]))))

    def get_offspring(self, x: int, y: int) -> Optional['EvolvingOrganism']:
        if self.food_count > constants.REPRODUCTION_COST:
            self.food_count = constants.START_FOOD
            return self.__get_offspring(x, y)
        return None
