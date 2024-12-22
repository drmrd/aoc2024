from aoc2024 import utilities
from aoc2024.maze import Maze


def solve_part_one():
    return min(
        score
        for _, score in Maze.from_map('\n'.join(utilities.input_lines(day=16)))
                            .find_best_paths().values()
    )


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())