import itertools
from collections import deque

from aoc2024 import utilities
from aoc2024.vector import Vector


def solve_part_one():
    return sum(
        max(lock + key) < 8
        for lock, key in itertools.product(*locks_and_keys())
    )


def solve_part_two():
    return 'Chronicle delivered!'


def locks_and_keys():
    schematics = '\n'.join(utilities.input_lines(day=25)).split('\n\n')
    locks, keys = deque(), deque()
    for schematic in schematics:
        rows = schematic.split('\n')
        signature = Vector(*(column.count('#') for column in list(zip(*rows))))
        (locks, keys)[rows[0] == '.....'].append(signature)
    return locks, keys


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())