from aoc2024.stone_simulator_2024 import stones_after


def test_stones_after_day11_part1_example1():
    total_stones = sum(
        stones_after(stone, 1)
        for stone in [0, 1, 10, 99, 999]
    )
    assert total_stones == len([1, 2024, 1, 0, 9, 9, 2021976])


def test_stones_after_day11_part1_example2():
    initial_stones = [125, 17]

    expected_blink_progression = [
        initial_stones,
        [253000, 1, 7],
        [253, 0, 2024, 14168],
        [512072, 1, 20, 24, 28676032],
        [512, 72, 2024, 2, 0, 2, 4, 2867, 6032],
        [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32],
        [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]
    ]
    for blinks, expected_stones in enumerate(expected_blink_progression):
        total_stones = sum(
            stones_after(initial_stone, blinks)
            for initial_stone in initial_stones
        )
        assert total_stones == len(expected_stones)