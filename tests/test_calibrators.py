import pytest

from aoc2024.calibrators import (
    is_calibrated,
    potential_addition,
    addition_partial_inverse,
    potential_multiplication,
    multiplication_partial_inverse,
    potential_concatenation,
    concatenation_partial_inverse
)


@pytest.fixture
def example_calibration_tests():
    return [
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


def test_is_calibrated_day7_part1_example(example_calibration_tests):
    sum_of_calibrated_test_values = sum(
        test_value
        for test_value, operands in example_calibration_tests
        if is_calibrated(
            test_value,
            operands,
            predicate_partial_inverse_pairs=[
                (potential_addition, addition_partial_inverse),
                (potential_multiplication, multiplication_partial_inverse)
            ]
        )
    )

    assert sum_of_calibrated_test_values == 3749


def test_is_calibrated_day7_part2_example(example_calibration_tests):
    sum_of_calibrated_test_values = sum(
        test_value
        for test_value, operands in example_calibration_tests
        if is_calibrated(
            test_value,
            operands,
            predicate_partial_inverse_pairs=[
                (potential_addition, addition_partial_inverse),
                (potential_multiplication, multiplication_partial_inverse),
                (potential_concatenation, concatenation_partial_inverse)
            ]
        )
    )

    assert sum_of_calibrated_test_values == 11387