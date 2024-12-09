from aoc2024.guard_simulator_2024 import GuardedLab


def test_guarded_lab_day6_part1_example():
    lab = GuardedLab([
        '....#.....',
        '.........#',
        '..........',
        '..#.......',
        '.......#..',
        '..........',
        '.#..^.....',
        '........#.',
        '#.........',
        '......#...'
    ])

    *_, lab = iter(lab)

    assert lab.visited_count == 41