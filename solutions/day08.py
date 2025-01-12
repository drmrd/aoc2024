import itertools

from aoc2024 import (
    easter_bunny_countermeasures as ebc,
    utilities
)
from aoc2024.vector import Vector


def solve_part_one():
    puzzle_input = list(utilities.input_lines(year=2024, day=8))

    mind_controlled_by_frequency = ebc.imc_mind_control_nearest_locations(
        antennae_by_frequency={
            frequency: list(set(
                Vector(row, column)
                for row in range(len(puzzle_input))
                for column in range(len(puzzle_input[0]))
                if puzzle_input[row][column] == frequency
            ))
            for frequency in set(''.join(puzzle_input)) - {'.'}
        },
        grid_shape=(len(puzzle_input), len(puzzle_input[0]))
    )
    mind_controlled_locations = set(
        itertools.chain.from_iterable(
            mind_controlled_by_frequency.values()
        )
    )
    return len(mind_controlled_locations)


def solve_part_two():
    puzzle_input = list(utilities.input_lines(year=2024, day=8))

    mind_controlled_by_frequency = ebc.imc_mind_control_locations(
        antennae_by_frequency={
            frequency: list(set(
                Vector(row, column)
                for row in range(len(puzzle_input))
                for column in range(len(puzzle_input[0]))
                if puzzle_input[row][column] == frequency
            ))
            for frequency in set(''.join(puzzle_input)) - {'.'}
        },
        grid_shape=(len(puzzle_input), len(puzzle_input[0]))
    )
    mind_controlled_locations = set(
        itertools.chain.from_iterable(
            mind_controlled_by_frequency.values()
        )
    )
    return len(mind_controlled_locations)


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())