from aoc2024.location_ids import compare_lists


def test_day01_example():
    assert compare_lists([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]) == 11