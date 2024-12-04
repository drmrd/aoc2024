from aoc2024 import compuboggan, utilities


def solve_part_one():
    source_code = '\n'.join(utilities.input_lines(day=3))
    return compuboggan.eval(source_code)


def solve_part_two():
    source_code = '\n'.join(utilities.input_lines(day=3))
    return compuboggan.eval(source_code)


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())