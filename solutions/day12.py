import itertools

from aoc2024 import utilities
from aoc2024.modern_garden import fence_cost


def solve_part_one():
    garden_grid = [
        list(garden_line) for garden_line in utilities.input_lines(day=12)
    ]
    garden_shape = (len(garden_grid), len(garden_grid[0]))
    return fence_cost({
        (row, column): garden_grid[row][column]
        for row, column in itertools.product(*map(range, garden_shape))
    })


def solve_part_two():
    garden_grid = [
        list(garden_line) for garden_line in utilities.input_lines(day=12)
    ]
    garden_shape = (len(garden_grid), len(garden_grid[0]))
    return fence_cost(
        {
            (row, column): garden_grid[row][column]
            for row, column in itertools.product(*map(range, garden_shape))
        },
        bulk_discount=True
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())