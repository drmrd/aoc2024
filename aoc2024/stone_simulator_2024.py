import math
from functools import cache


@cache
def stones_after(initial: int, blinks: int) -> int:
    if not blinks:
        return 1
    if not initial:
        return stones_after(1, blinks - 1)
    if not (digits := math.ceil(math.log10(initial + 1))) % 2:
        return sum(
            stones_after(half_of_digits, blinks - 1)
            for half_of_digits in divmod(
                initial, 10 ** (digits // 2)
            )
        )
    return stones_after(2024 * initial, blinks - 1)