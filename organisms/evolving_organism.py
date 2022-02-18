from typing import Tuple, Optional, List, Dict
from random import random, choice

from direction import Direction
from entity import Entity
import constants


class EvolvingOrganism(Entity):
    def __init__(self, x: int, y: int, sight: int = 1, speed: int = 1,
                 color: Tuple[int, int, int] = (127, 127, 127)) -> None:
        super().__init__(x, y, constants.ORGANISM_ID, color)
        self.food_count: float = constants.START_FOOD
        self.age = 0
        self.max_age = constants.MAX_AGE
        self.sight = sight
        self.speed = speed

    def get_no_move_probability(self) -> float:
        return self.age / self.max_age

    def get_moves(self, sight: Dict[Direction, list]) -> List[Direction]:
        # TODO: change sight to color of entity with highest mask id and then use some algorithm to determine which direction is most desirable based on how similar color is to food and distance
        self.food_count -= constants.COST_TO_LIVE * self.sight
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
        for direction, data in sight.items():
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
            return False
        red = color[0]
        green = color[1]
        blue = color[2]
        color_score = ((green - red + 255) / (255 * 2) + (green - blue + 255) / (255 * 2)) / 2
        distance_score = ((distance - 1) / (self.sight - 1 if self.sight > 1 else 1) * -1) + 1
        score = color_score + distance_score
        return score

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

    def __get_offspring(self, x: int, y: int) -> Optional['EvolvingOrganism']:
        sight_delta = choice([-1, 1])
        new_sight = self.sight + sight_delta
        return EvolvingOrganism(x, y, sight=new_sight, speed=self.speed + choice([-1, 1]), color=(
            self.clamp_color_value(self.color[0] + choice([-10, 10])),
            self.clamp_color_value(self.color[1] + choice([-10, 10])),
            self.clamp_color_value(self.color[2] + choice([-10, 10]))))

    def get_offspring(self, x: int, y: int) -> Optional['EvolvingOrganism']:
        if self.food_count > constants.REPRODUCTION_COST:
            self.food_count = constants.START_FOOD
            return self.__get_offspring(x, y)
        return None
