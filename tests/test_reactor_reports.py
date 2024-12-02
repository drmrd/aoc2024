import pytest

from aoc2024 import reactor_reports


@pytest.mark.parametrize(
    ['report', 'safety'],
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], False),
        ([8, 6, 4, 4, 1], False),
        ([1, 3, 6, 7, 9], True)
    ]
)
def test_is_safe_day2_example(report, safety):
    assert reactor_reports.is_safe(report) == safety