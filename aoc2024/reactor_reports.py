import itertools
import math


def is_safe(report: list[int]) -> bool:
    return is_strictly_safe(report) or any(
        is_strictly_safe([
            level
            for level_index, level in enumerate(report)
            if level_index != ignored_index
        ])
        for ignored_index in range(len(report))
    )


def is_strictly_safe(report: list[int]) -> bool:
    def sign(x: float) -> float:
        return math.copysign(1, x)

    differences = {
        second - first for first, second in itertools.pairwise(report)
    }
    signs = {sign(difference) for difference in differences}
    absolute_differences = {abs(difference) for difference in differences}

    return len(signs) == 1 and absolute_differences <= {1, 2, 3}