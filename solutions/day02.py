from aoc2024 import reactor_reports, utilities


def solve_part_one():
    reports = utilities.input_grid(year=2024, day=2, colsep=' ', caster=int)
    return sum(reactor_reports.is_strictly_safe(report) for report in reports)


def solve_part_two():
    reports = utilities.input_grid(year=2024, day=2, colsep=' ', caster=int)
    return sum(reactor_reports.is_safe(report) for report in reports)


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())