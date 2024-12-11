from aoc2024 import utilities
from aoc2024.calibrators import (
    is_calibrated,
    potential_addition,
    addition_partial_inverse,
    potential_multiplication,
    multiplication_partial_inverse,
    potential_concatenation,
    concatenation_partial_inverse
)


def solve_part_one():
    calibration_tests = (
        (int(test_value), tuple(int(operand) for operand in operands.split(' ')))
        for test_value, operands in map(
            lambda equation: equation.split(': '),
            utilities.input_lines(day=7)
        )
    )
    return sum(
        test_value
        for test_value, operands in calibration_tests
        if is_calibrated(
            test_value, operands,
            predicate_partial_inverse_pairs=[
                (potential_addition, addition_partial_inverse),
                (potential_multiplication, multiplication_partial_inverse)
            ]
        )
    )


def solve_part_two():
    calibration_tests = (
        (int(test_value), tuple(int(operand) for operand in operands.split(' ')))
        for test_value, operands in map(
            lambda equation: equation.split(': '),
            utilities.input_lines(day=7)
        )
    )
    return sum(
        test_value
        for test_value, operands in calibration_tests
        if is_calibrated(
            test_value, operands,
            predicate_partial_inverse_pairs=[
                (potential_addition, addition_partial_inverse),
                (potential_multiplication, multiplication_partial_inverse),
                (potential_concatenation, concatenation_partial_inverse)
            ]
        )
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())