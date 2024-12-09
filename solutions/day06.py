from aoc2024 import utilities
from aoc2024.guard_simulator_2024 import GuardedLab


def solve_part_one():
    *_, lab = iter(GuardedLab(list(utilities.input_lines(day=6))))
    return lab.visited_count


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())