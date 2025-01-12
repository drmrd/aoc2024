import functools
import itertools
import operator
import re

from aoc2024 import utilities
from aoc2024.vector import Vector


def solve_part_one():
    foyer_width, foyer_length = foyer_shape = Vector(101, 103)
    robots = robot_guards()
    for _ in range(100):
        for robot in robots:
            robot['position'] = (
                robot['position'] + robot['velocity']
            ) % foyer_shape
    quadrant_count = {
        quadrant: 0 for quadrant in itertools.product((True, False), repeat=2)
    }
    for robot in robots:
        x, y = robot['position']
        if x != foyer_width // 2 and y != foyer_length // 2:
            quadrant_count[x > foyer_width // 2, y > foyer_length // 2] += 1
    return functools.reduce(operator.mul, quadrant_count.values(), 1)


def solve_part_two():
    foyer_shape = Vector(101, 103)
    robots = robot_guards()
    for seconds in range(1, 10_000):
        for robot in robots:
            robot['position'] = (
                robot['position'] + robot['velocity']
            ) % foyer_shape
        for (x, y) in (positions := {robot['position'] for robot in robots}):
            other_tree_positions = {
                *((x + offset, y + 1) for offset in range(-1, 2)),
                *((x + offset, y + 2) for offset in range(-2, 3))
            }
            free_positions = (
                {
                    (x + x_offset, y + y_offset)
                    for x_offset in range(-2, 3)
                    for y_offset in range(2)
                } - ({(x, y)} | other_tree_positions)
            )
            if (
                other_tree_positions.issubset(positions)
                and positions.isdisjoint(free_positions)
            ):
                return seconds
    return float('inf')


def robot_guards():
    return [
        {
            'position': Vector(*map(int, robot.groups()[:2])),
            'velocity': Vector(*map(int, robot.groups()[2:]))
        }
        for robot in re.finditer(
            r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)',
            '\n'.join(utilities.input_lines(year=2024, day=14))
        )
    ]


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())