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
def test_input_grid_returns_list_of_lists(monkeypatch, tmp_path, input_content, row_separator, column_separator, entry_caster, expected_grid):
    monkeypatch.setattr(
        utilities, 'PUZZLE_INPUTS_DIRECTORY', tmp_path / 'puzzle_inputs'
    )
    puzzle_inputs_dir = tmp_path / 'puzzle_inputs'
    puzzle_inputs_dir.mkdir()
    puzzle_day = 7
    (puzzle_inputs_dir / f'Day_{puzzle_day:0>2}.txt').write_text(
        row_separator.join(map(column_separator.join, input_content))
    )

    actual_input_grid = utilities.input_grid(
        day=puzzle_day, rowsep=row_separator, colsep=column_separator,
        caster=entry_caster
    )
    assert actual_input_grid == expected_grid


def test_input_lines_returns_each_line_of_input_file_as_string(monkeypatch, tmp_path):
    monkeypatch.setattr(
        utilities, 'PUZZLE_INPUTS_DIRECTORY', tmp_path / 'puzzle_inputs'
    )
    puzzle_inputs_dir = tmp_path / 'puzzle_inputs'
    puzzle_inputs_dir.mkdir()
    puzzle_day = 3
    expected_input_lines = [f'input line {number}' for number in range(10)]
    (puzzle_inputs_dir / f'Day_{puzzle_day:0>2}.txt').write_text(
        '\n'.join(expected_input_lines)
    )

    assert list(utilities.input_lines(puzzle_day)) == expected_input_lines