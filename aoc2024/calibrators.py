from collections.abc import Iterable


def is_calibrated(test_value: int, operands: Iterable[int]) -> bool:
    *all_but_last, last = operands
    if not all_but_last:
        return test_value == last
    return (
        is_calibrated(test_value - last, all_but_last)
        or (
            (test_value % last == 0)
            and is_calibrated(test_value // last, all_but_last)
        )
    )