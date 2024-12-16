from aoc2024 import utilities
from aoc2024.stone_simulator_2024 import StoneSimulator2024


def solve_part_one():
    stone_simulator = StoneSimulator2024(
        map(int, next(utilities.input_lines(day=11)).split())
    )
    for _ in range(25):
        stone_simulator = stone_simulator.blink()
    return len(tuple(stone_simulator))


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())