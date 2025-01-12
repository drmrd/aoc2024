import aocd
import pytest

from aoc2024 import utilities


@pytest.mark.parametrize(
    ('input_content', 'expected_grid', 'row_separator', 'column_separator', 'entry_caster'),
    [
        (
            [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']],
            [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']],
            '\n', ',', None
        ),
        (
            [['137', '2', '333'], 3 * ['-30', '8', '8675309'], 2 * ['38', '51', '52']],
            [[137, 2, 333], 3 * [-30, 8, 8675309], 2 * [38, 51, 52]],
            'weird sequence', ';', int
        )
    ]
)
def test_input_grid_returns_list_of_lists(monkeypatch, input_content, row_separator, column_separator, entry_caster, expected_grid):
    expected_text = row_separator.join(
        map(column_separator.join, input_content)
    )
    monkeypatch.setattr(
        aocd, 'get_data', lambda *args, **kwargs: expected_text
    )

    actual_input_grid = utilities.input_grid(
        year=2024, day=23, rowsep=row_separator, colsep=column_separator,
        caster=entry_caster
    )
    assert actual_input_grid == expected_grid


def test_input_lines_returns_each_line_of_input_file_as_string(monkeypatch):
    expected_input_lines = [f'input line {number}' for number in range(10)]
    expected_text = '\n'.join(expected_input_lines)
    monkeypatch.setattr(
        aocd, 'get_data', lambda *args, **kwargs: expected_text
    )

    assert list(utilities.input_lines(year=2024, day=4)) == expected_input_lines