from aoc2024 import utilities


def test_input_grid_returns_list_of_lists(monkeypatch, tmp_path):
    monkeypatch.setattr(
        utilities, 'PUZZLE_INPUTS_DIRECTORY', tmp_path / 'puzzle_inputs'
    )
    puzzle_inputs_dir = tmp_path / 'puzzle_inputs'
    puzzle_inputs_dir.mkdir()
    puzzle_day = 7
    puzzle_grid = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]
    (puzzle_inputs_dir / f'Day_{puzzle_day:0>2}.txt').write_text(
        '\n'.join(map(','.join, puzzle_grid))
    )

    assert utilities.input_grid(day=puzzle_day) == puzzle_grid


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