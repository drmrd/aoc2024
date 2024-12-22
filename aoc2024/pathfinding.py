from __future__ import annotations

import math
from enum import Enum
from functools import cached_property, lru_cache, cache

from aoc2024.vector import Vector


class Direction(Enum):
    UP = -1
    DOWN = 1
    LEFT = -1j
    RIGHT = 1j

    @cache
    def __lt__(self, other):
        if self.value.real < other.value.real:
            return True
        else:
            return self.value.imag < other.value.imag

    @cached_property
    def grid_offsets(self) -> tuple[int, int]:
        return int(self.value.real), int(self.value.imag)

    @cached_property
    def grid_vector(self) -> Vector[int]:
        return Vector(*self.grid_offsets)

    @lru_cache(4)
    def rotate_counterclockwise(self) -> Direction:
        return Direction(self.value * 1j)

    @lru_cache(4)
    def rotate_clockwise(self) -> Direction:
        return Direction(self.value * -1j)

    @cached_property
    def principal_argument(self) -> float:
        return math.atan2(self.value.imag, self.value.real)

    @classmethod
    @lru_cache(16)
    def from_caret(cls, caret: str) -> Direction:
        try:
            return {
                '^': cls.UP, 'v': cls.DOWN, '<': cls.LEFT, '>': cls.RIGHT
            }[caret]
        except KeyError:
            raise ValueError(f'Unknown direction caret "{caret}".')