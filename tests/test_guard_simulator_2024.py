import pytest

from aoc2024.guard_simulator_2024 import GuardedLab


@pytest.fixture
def day6_example_lab_state() -> list[str]:
    return [
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
    ]


def test_guarded_lab_day6_part1_example(day6_example_lab_state):
    lab = GuardedLab(day6_example_lab_state)

    *_, lab = iter(lab)

    assert lab.visited_count == 41


def test_resetting_lab_removes_guard_and_visited_positions(day6_example_lab_state):
    lab = GuardedLab(day6_example_lab_state)
    for _ in zip(lab, range(5)):
        continue

    lab.reset()

    assert lab.visited_count == 0
    assert not lab.is_guarded
    with pytest.raises(ValueError, match='unguarded'):
        lab.guard_position
    with pytest.raises(ValueError, match='unguarded'):
        lab.guard_orientation