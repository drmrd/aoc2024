import itertools
import math


def is_safe(report: list[int]) -> bool:
    def sign(n: int):
        return math.copysign(1, n)

    first_sign = sign(report[1] - report[0])

    return all(
        (sign(second - first) == first_sign)
        and
        (1 <= abs(second - first) <= 3)
        for first, second in itertools.pairwise(report)
    )