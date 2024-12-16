from aoc2024 import utilities
from aoc2024.stone_simulator_2024 import stones_after


def solve_part_one():
    return sum(
        stones_after(stone, 25)
        for stone in map(int, next(utilities.input_lines(day=11)).split())
    )


def solve_part_two():
    return sum(
        stones_after(stone, 75)
        for stone in map(int, next(utilities.input_lines(day=11)).split())
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())