from __future__ import annotations

import itertools
from collections.abc import Callable

import pytest

from aoc2024.modern_garden import (
    area, edges, fence_cost, garden_regions, perimeter
)


def mapping_fixture[T](
        grid: list[list[T]]
) -> Callable[[], dict[tuple[int, int], T]]:
    @pytest.fixture
    def mapping_fixture_from_grid() -> dict[tuple[int, int], T]:
        grid_shape = (len(grid), len(grid[0]))
        return {
            (row, column): grid[row][column]
            for row, column in itertools.product(*map(range, grid_shape))
        }
    return mapping_fixture_from_grid


garden_day12_part1_example1 = mapping_fixture([
    ['A', 'A', 'A', 'A'],
    ['B', 'B', 'C', 'D'],
    ['B', 'B', 'C', 'C'],
    ['E', 'E', 'E', 'C']
])
garden_day12_part1_example2 = mapping_fixture([
    ['O', 'O', 'O', 'O', 'O'],
    ['O', 'X', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O', 'O'],
    ['O', 'X', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O', 'O']
])
garden_day12_part1_example3 = mapping_fixture([
    ['R', 'R', 'R', 'R', 'I', 'I', 'C', 'C', 'F', 'F'],
    ['R', 'R', 'R', 'R', 'I', 'I', 'C', 'C', 'C', 'F'],
    ['V', 'V', 'R', 'R', 'R', 'C', 'C', 'F', 'F', 'F'],
    ['V', 'V', 'R', 'C', 'C', 'C', 'J', 'F', 'F', 'F'],
    ['V', 'V', 'V', 'V', 'C', 'J', 'J', 'C', 'F', 'E'],
    ['V', 'V', 'I', 'V', 'C', 'C', 'J', 'J', 'E', 'E'],
    ['V', 'V', 'I', 'I', 'I', 'C', 'J', 'J', 'E', 'E'],
    ['M', 'I', 'I', 'I', 'I', 'I', 'J', 'J', 'E', 'E'],
    ['M', 'I', 'I', 'I', 'S', 'I', 'J', 'E', 'E', 'E'],
    ['M', 'M', 'M', 'I', 'S', 'S', 'J', 'E', 'E', 'E']
])


def test_garden_regions_day12_part1_example1(garden_day12_part1_example1):
    expected_regions = {
        frozenset({(0, 0), (0, 1), (0, 2), (0, 3)}),
        frozenset({(1, 0), (1, 1), (2, 0), (2, 1)}),
        frozenset({(1, 2), (2, 2), (2, 3), (3, 3)}),
        frozenset({(1, 3)}),
        frozenset({(3, 0), (3, 1), (3, 2)})
    }
    assert garden_regions(garden_day12_part1_example1) == expected_regions


def test_garden_regions_day12_part1_example2(garden_day12_part1_example2):
    assert sorted(
        len(region)
        for region in garden_regions(garden_day12_part1_example2)
    ) == [1, 1, 1, 1, 21]


def test_area_day12_part1_example1():
    regions = [
        frozenset({(0, 0), (0, 1), (0, 2), (0, 3)}),
        frozenset({(1, 0), (1, 1), (2, 0), (2, 1)}),
        frozenset({(1, 2), (2, 2), (2, 3), (3, 3)}),
        frozenset({(1, 3)}),
        frozenset({(3, 0), (3, 1), (3, 2)})
    ]
    for region in regions:
        assert area(region) == len(region)


@pytest.mark.parametrize(
    ['region', 'expected_edges'],
    [
        (frozenset({(0, 0), (0, 1), (0, 2), (0, 3)}), 4),
        (frozenset({(1, 0), (1, 1), (2, 0), (2, 1)}), 4),
        (frozenset({(1, 2), (2, 2), (2, 3), (3, 3)}), 8),
        (frozenset({(1, 3)}), 4),
        (frozenset({(3, 0), (3, 1), (3, 2)}), 4),
    ]
)
def test_edges_day12_part1_example1(region, expected_edges):
    assert edges(region) == expected_edges


def test_perimeter_day12_part1_example1():
    expected_perimeter_by_region = {
        frozenset({(0, 0), (0, 1), (0, 2), (0, 3)}): 10,
        frozenset({(1, 0), (1, 1), (2, 0), (2, 1)}): 8,
        frozenset({(1, 2), (2, 2), (2, 3), (3, 3)}): 10,
        frozenset({(1, 3)}): 4,
        frozenset({(3, 0), (3, 1), (3, 2)}): 8
    }
    for region, expected_perimeter in expected_perimeter_by_region.items():
        assert perimeter(region) == expected_perimeter


def test_fence_cost_day12_part1_example1(garden_day12_part1_example1):
    assert fence_cost(garden_day12_part1_example1) == 140


def test_fence_cost_day12_part1_example2(garden_day12_part1_example2):
    assert fence_cost(garden_day12_part1_example2) == 772


def test_fence_cost_day12_part1_example3(garden_day12_part1_example3):
    assert fence_cost(garden_day12_part1_example3) == 1930
