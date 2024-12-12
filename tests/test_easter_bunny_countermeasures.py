import itertools

import pytest

import aoc2024.easter_bunny_countermeasures as ebc
from aoc2024.vector import Vector


@pytest.fixture
def example_puzzle_input() -> list[str]:
    return [
        '............',
        '........0...',
        '.....0......',
        '.......0....',
        '....0.......',
        '......A.....',
        '............',
        '............',
        '........A...',
        '.........A..',
        '............',
        '............'
    ]


def test_day8_part1_example(example_puzzle_input):
    mind_controlled_by_frequency = ebc.imc_mind_control_nearest_locations(
        antennae_by_frequency={
            frequency: list(set(
                Vector(row, column)
                for row in range(len(example_puzzle_input))
                for column in range(len(example_puzzle_input[0]))
                if example_puzzle_input[row][column] == frequency
            ))
            for frequency in set(''.join(example_puzzle_input)) - {'.'}
        },
        grid_shape=(len(example_puzzle_input), len(example_puzzle_input[0]))
    )
    nearest_mind_controlled_locations = set(
        itertools.chain.from_iterable(
            mind_controlled_by_frequency.values()
        )
    )
    assert len(nearest_mind_controlled_locations) == 14


def test_day8_part2_example(example_puzzle_input):
    mind_controlled_by_frequency = ebc.imc_mind_control_locations(
        antennae_by_frequency={
            frequency: list(set(
                Vector(row, column)
                for row in range(len(example_puzzle_input))
                for column in range(len(example_puzzle_input[0]))
                if example_puzzle_input[row][column] == frequency
            ))
            for frequency in set(''.join(example_puzzle_input)) - {'.'}
        },
        grid_shape=(len(example_puzzle_input), len(example_puzzle_input[0]))
    )
    mind_controlled_locations = set(
        itertools.chain.from_iterable(
            mind_controlled_by_frequency.values()
        )
    )
    assert len(mind_controlled_locations) == 34