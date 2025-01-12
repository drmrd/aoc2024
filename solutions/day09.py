from aoc2024 import utilities
from aoc2024.defrag import DiskMap


def solve_part_one():
    return (
        DiskMap.from_dense_map(next(utilities.input_lines(year=2024, day=9)))
               .back_fill()
               .checksum
    )


def solve_part_two():
    return (
        DiskMap.from_dense_map(next(utilities.input_lines(year=2024, day=9)))
               .defrag()
               .checksum
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())