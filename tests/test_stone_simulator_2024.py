from aoc2024.stone_simulator_2024 import StoneSimulator2024


def test_stone_simulator_day11_part1_example1():
    stone_simulator = StoneSimulator2024([0, 1, 10, 99, 999])
    assert list(stone_simulator.blink()) == [1, 2024, 1, 0, 9, 9, 2021976]


def test_stone_simulator_day11_part1_example2():
    stone_simulator = StoneSimulator2024([125, 17])

    expected_blink_progression = [
        [253000, 1, 7],
        [253, 0, 2024, 14168],
        [512072, 1, 20, 24, 28676032],
        [512, 72, 2024, 2, 0, 2, 4, 2867, 6032],
        [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32],
        [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]
    ]
    for expected_stones in expected_blink_progression:
        stone_simulator = stone_simulator.blink()
        assert list(stone_simulator) == expected_stones