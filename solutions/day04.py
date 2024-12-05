from aoc2024 import word_search, utilities


def solve_part_one():
    puzzle = '\n'.join(utilities.input_lines(day=4))
    return word_search.count(puzzle, words=['XMAS'])


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())