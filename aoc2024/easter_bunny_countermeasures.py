import itertools
from collections.abc import Collection, Sequence

from aoc2024.vector import Vector


def imc_mind_control_locations(
        antennae_by_frequency: dict[str, Sequence[Vector[int]]],
        grid_shape
) -> dict[str, Collection[Vector[int]]]:
    return {
        frequency: _antinodes(antennae, grid_shape)
        for frequency, antennae in antennae_by_frequency.items()
    }


def _antinodes(
        antennae: Sequence[Vector[int]],
        upper_bounds: tuple[int, int]
) -> Collection[Vector[int]]:
    match antennae:
        case [*locations] if len(locations) < 2:
            raise ValueError('At least two antennae locations are required.')
        case [antenna1, antenna2] if antenna1 == antenna2:
            raise ValueError('Antennae must be unique.')
        case [antenna1, antenna2]:
            delta = antenna2 - antenna1
            possible_antinodes = [antenna1 - delta, antenna2 + delta]
            return {
                antinode
                for antinode in possible_antinodes
                if min(antinode) >= 0
                   and antinode[0] < upper_bounds[0]
                   and antinode[1] < upper_bounds[1]
            }
        case _:
            return set(
                itertools.chain.from_iterable(
                    _antinodes(antenna_pair, upper_bounds)
                    for antenna_pair in itertools.combinations(antennae, r=2)
                )
            )