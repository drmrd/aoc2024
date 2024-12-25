from functools import cache

from aoc2024 import utilities


@cache
def is_arrangement(design: str, patterns: tuple[str, ...]) -> bool:
    if not design:
        return True
    return any(
        is_arrangement(design[len(pattern):], patterns)
        for pattern in patterns
        if design.startswith(pattern)
    )


def solve_part_one():
    puzzle_input = utilities.input_lines(day=19)
    patterns = tuple(
        sorted(
            next(puzzle_input).split(', '),
            key=lambda pattern: -len(pattern)
        )
    )
    next(puzzle_input)
    requested_designs = sorted(set(puzzle_input), key=len)

    return sum(
        is_arrangement(design, patterns) for design in requested_designs
    )


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())