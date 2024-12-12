import itertools
from collections.abc import Collection, Iterable, Sequence

from aoc2024.vector import Vector


def imc_mind_control_locations(
        antennae_by_frequency: dict[str, Sequence[Vector[int]]],
        grid_shape
) -> dict[str, Collection[Vector[int]]]:
    return {
        frequency: _antinodes_in_grid(antennae, grid_shape)
        for frequency, antennae in antennae_by_frequency.items()
    }


def imc_mind_control_nearest_locations(
        antennae_by_frequency: dict[str, Sequence[Vector[int]]],
        grid_shape
) -> dict[str, Collection[Vector[int]]]:
    return {
        frequency: _antinodes_in_grid(antennae, grid_shape, only_neighbors=True)
        for frequency, antennae in antennae_by_frequency.items()
    }


def _antinodes_in_grid(
        antennae: Sequence[Vector[int]],
        upper_bounds: tuple[int, int],
        only_neighbors: bool = False
) -> Collection[Vector[int]]:
    match antennae:
        case [*locations] if len(locations) < 2:
            raise ValueError('At least two antennae locations are required.')
        case [antenna1, antenna2] if antenna1 == antenna2:
            raise ValueError('Antennae must be unique.')
        case [antenna1, antenna2]:
            if only_neighbors:
                delta = antenna2 - antenna1
                possible_antinodes = [antenna1 - delta, antenna2 + delta]
                return {
                    antinode
                    for antinode in possible_antinodes
                    if min(antinode) >= 0
                       and antinode[0] < upper_bounds[0]
                       and antinode[1] < upper_bounds[1]
                }
            else:
                return {
                    antinode
                    for antinode in _bounded_antinodes(
                        antenna1,
                        antenna2,
                        lower_bounds=(0, 0),
                        upper_bounds=upper_bounds
                    )
                }
        case _:
            return set(
                itertools.chain.from_iterable(
                    _antinodes_in_grid(antenna_pair, upper_bounds, only_neighbors)
                    for antenna_pair in itertools.combinations(antennae, r=2)
                )
            )


def _bounded_antinodes(
        antenna1: Vector[int],
        antenna2: Vector[int],
        lower_bounds: tuple[int, int],
        upper_bounds: tuple[int, int]
) -> Iterable[Vector[int]]:
    def in_bounds(antinode: Vector[int]) -> bool:
        return all(
            lower_bounds[index] <= antinode[index] < upper_bounds[index]
            for index in range(2)
        )

    delta = antenna2 - antenna1
    for starting_antinode, delta in [(antenna2, delta), (antenna1, -delta)]:
        antinode = starting_antinode
        while in_bounds(antinode):
            yield antinode
            antinode += delta