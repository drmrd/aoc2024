from __future__ import annotations

import itertools
import math
import re
from enum import Enum
from functools import cache, cached_property

from aoc2024 import utilities
from aoc2024.vector import Vector


class Keypad(Enum):
    NUM = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A']
    ]
    DIR = [
        [None, '^', 'A'],
        ['<', 'v', '>']
    ]

    @cache
    def location(self, key: str | None) -> Vector[int]:
        for row_index, row in enumerate(self.value):
            try:
                return Vector(row_index, row.index(key))
            except ValueError:
                continue
        raise ValueError(f'Key {key} not found in keypad {self.name}.')

    @cache
    def shortest_path(self, start, stop):
        start_row, start_col = start_loc = self.location(start)
        stop_row, stop_col = stop_loc = self.location(stop)
        blank_row, blank_col = self.location(None)
        row_offset, col_offset = stop_loc - start_loc

        horizontal_part = abs(col_offset) * ('<' if col_offset < 0 else '>')
        vertical_part = abs(row_offset) * ('^' if row_offset < 0 else 'v')

        # This is logic can be simplified for the specific keypads in Day 21,
        # but I decided to leave it more complete here for fun.
        can_move_left_initially = (
            blank_col < stop_col
            or
            (
                blank_col == stop_col
                and sign(blank_row - start_row) == sign(blank_row - stop_row)
            )
            or (blank_col > stop_col and blank_row != start_row)
        )
        if (
                (can_move_left_initially and col_offset < 0)
                or start_col == blank_col
        ):
            return f'{horizontal_part}{vertical_part}'
        else:
            return f'{vertical_part}{horizontal_part}'

    @cached_property
    def keys(self) -> list[str]:
        return [key for row in self.value for key in row if key is not None]

    @cached_property
    def key_count(self) -> int:
        return sum(key is not None for row in self.value for key in row)

    @classmethod
    def total_keys(cls):
        return sum(keypad.key_count for keypad in cls)


def sign(x: float) -> float:
    return math.copysign(1, x) if x else 0


@cache
def all_keypad_paths(keypad: Keypad) -> dict[tuple[str, str], str]:
    return {
        (key1, key2): f'{keypad.shortest_path(key1, key2)}A'
        for key1 in keypad.keys
        for key2 in keypad.keys
        if key1 is not None and key2 is not None
    }


@cache
def chained_controller_sequence_length(
        key_sequence: str,
        remaining_dirpads: int,
        at_numpad: bool = True
) -> int:
    if remaining_dirpads == 0:
        return len(key_sequence)
    if at_numpad:
        keypad_paths = all_keypad_paths(Keypad.NUM)
    else:
        keypad_paths = all_keypad_paths(Keypad.DIR)

    key_sequence_pairs = itertools.chain(
        [('A', key_sequence[0])],
        itertools.pairwise(key_sequence)
    )
    return sum(
        chained_controller_sequence_length(
            key_sequence=keypad_paths[previous_key, current_key],
            remaining_dirpads=remaining_dirpads - (not at_numpad),
            at_numpad=False
        )
        for previous_key, current_key in key_sequence_pairs
    )


def complexity(code: str, directional_robots: int) -> int:
    return (
        int(re.sub(r'^(\d+).*$', r'\1', code))
        * chained_controller_sequence_length(code, directional_robots)
    )


def solve_part_one():
    return sum(
        complexity(code, directional_robots=2)
        for code in utilities.input_lines(year=2024, day=21)
    )


def solve_part_two():
    return sum(
        complexity(code, directional_robots=25)
        for code in utilities.input_lines(year=2024, day=21)
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())