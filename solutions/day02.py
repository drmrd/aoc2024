from aoc2024 import reactor_reports, utilities


def solution_to_part_one():
    reports = (
        [int(level) for level in report.split()]
        for report in utilities.input_lines(day=2)
    )
    return sum(reactor_reports.is_safe(report) for report in reports)


if __name__ == '__main__':
    print('Solution to Part 1:', solution_to_part_one())