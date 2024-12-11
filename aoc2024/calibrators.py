from collections.abc import Sequence, Callable
from typing import Iterable


def is_calibrated(
        test_value: int,
        operands: Sequence[int],
        predicate_partial_inverse_pairs: Iterable[
            tuple[Callable[[int, int], bool], Callable[[int, int], int]]
        ]
) -> bool:
    *all_but_last, last = operands
    if not all_but_last:
        return test_value == last

    return any(
        is_calibrated(
            partial_inverse(test_value, last),
            all_but_last,
            predicate_partial_inverse_pairs
        )
        for predicate, partial_inverse in predicate_partial_inverse_pairs
        if predicate(test_value, last)
    )


def potential_addition(test_value: int, last_operand: int) -> bool:
    return last_operand < test_value


def addition_partial_inverse(test_value: int, last_operand: int) -> int:
    return test_value - last_operand


def potential_multiplication(test_value: int, last_operand: int) -> bool:
    return test_value % last_operand == 0


def multiplication_partial_inverse(test_value: int, last_operand: int) -> int:
    return test_value // last_operand


def potential_concatenation(test_value: int, last_operand: int) -> bool:
    test_value_string = str(test_value)
    last_operand_string = str(last_operand)
    return (
        len(test_value_string) != len(last_operand_string)
        and test_value_string[-len(last_operand_string):] == last_operand_string
    )


def concatenation_partial_inverse(test_value: int, last_operand: int) -> int:
    return int(str(test_value)[:-len(str(last_operand))])