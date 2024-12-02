from aoc2024 import reactor_reports, utilities


def solve_part_one():
    reports = (
        [int(level) for level in report.split()]
        for report in utilities.input_lines(day=2)
    )
    return sum(reactor_reports.is_strictly_safe(report) for report in reports)


def solve_part_two():
    reports = (
        [int(level) for level in report.split()]
        for report in utilities.input_lines(day=2)
    )
    return sum(reactor_reports.is_safe(report) for report in reports)


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())