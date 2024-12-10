from aoc2024.calibrators import is_calibrated


def test_is_calibrated_day7_part1_example():
    example_calibration_tests = [
        (190, (10, 19)),
        (3267, (81, 40, 27)),
        (83, (17, 5)),
        (156, (15, 6)),
        (7290, (6, 8, 6, 15)),
        (161011, (16, 10, 13)),
        (192, (17, 8, 14)),
        (21037, (9, 7, 18, 13)),
        (292, (11, 6, 16, 20))
    ]

    sum_of_calibrated_test_values = sum(
        test_value
        for test_value, operands in example_calibration_tests
        if is_calibrated(test_value, operands)
    )

    assert sum_of_calibrated_test_values == 3749