import itertools

from aoc2024.modern_garden import area, garden_regions


def test_garden_regions_day12_part1_example1():
    garden_plants = [
        ['A', 'A', 'A', 'A'],
        ['B', 'B', 'C', 'D'],
        ['B', 'B', 'C', 'C'],
        ['E', 'E', 'E', 'C']
    ]
    garden = {
        (row, column): garden_plants[row][column]
        for row, column in itertools.product(range(4), range(4))
    }

    expected_regions = {
        frozenset({(0, 0), (0, 1), (0, 2), (0, 3)}),
        frozenset({(1, 0), (1, 1), (2, 0), (2, 1)}),
        frozenset({(1, 2), (2, 2), (2, 3), (3, 3)}),
        frozenset({(1, 3)}),
        frozenset({(3, 0), (3, 1), (3, 2)})
    }
    assert garden_regions(garden) == expected_regions


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