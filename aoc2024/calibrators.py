from collections.abc import Sequence


def is_calibrated(
        test_value: int,
        operands: Sequence[int],
        part2: bool
) -> bool:
    *all_but_last, last = operands
    if not all_but_last:
        return test_value == last
    return (
        is_calibrated(test_value - last, all_but_last, part2)
        or (
            (test_value % last == 0)
            and is_calibrated(test_value // last, all_but_last, part2)
        )
        or (
            part2
            and
            test_value > 0
            and
            (
                (test_value_string := str(test_value))[
                    -len(last_string := str(last)):
                ]
            ) == last_string
            and (
                len(test_value_string) != len(last_string)
            )
            and is_calibrated(
                int(test_value_string[:-len(last_string)]),
                all_but_last,
                part2
            )
        )
    )