import re
from collections.abc import Iterator

from aoc2024 import utilities


def solve_part_one(epsilon=1e-20):
    total_cost = 0
    for x1, y1, x2, y2, x0, y0 in claw_machines():
        a, b = intersection_point((x1, x2, x0), (y1, y2, y0))
        if all(approximately_whole(presses, epsilon) for presses in (a, b)):
            total_cost += round(3 * a + b)
    return total_cost


def solve_part_two(epsilon=1e-20):
    ten_trillion = 10_000_000_000_000
    total_cost = 0
    for x1, y1, x2, y2, x0, y0 in claw_machines():
        a, b = intersection_point(
            (x1, x2, x0 + ten_trillion), (y1, y2, y0 + ten_trillion)
        )
        if all(approximately_whole(presses, epsilon) for presses in (a, b)):
            total_cost += round(3 * a + b)
    return total_cost


def claw_machines() -> Iterator[tuple[int, int, int, int, int, int]]:
    for claw_machine in re.finditer(
        '\n'.join([
            r'Button A: X\+(\d+), Y\+(\d+)',
            r'Button B: X\+(\d+), Y\+(\d+)',
            r'Prize: X=(\d+), Y=(\d+)'
        ]),
        '\n'.join(utilities.input_lines(day=13))
    ):
        yield tuple(
            int(coefficient) for coefficient in claw_machine.groups()
        )  # type: ignore


def intersection_point(
        line1: tuple[float, float, float], line2: tuple[float, float, float]
) -> tuple[float, float]:
    (x1, x2, x0), (y1, y2, y0) = line1, line2
    determinant = x1 * y2 - x2 * y1
    return (x0 * y2 - x2 * y0) / determinant, (x1 * y0 - x0 * y1) / determinant


def approximately_whole(x: float, tolerance) -> bool:
    return x + tolerance > 0 and abs(x - round(x)) < tolerance


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())