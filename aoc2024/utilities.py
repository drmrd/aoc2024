from collections.abc import Generator
from pathlib import Path


PUZZLE_INPUTS_DIRECTORY = Path.cwd() / 'puzzle_inputs'


def input_lines(day: int) -> Generator[str]:
    with (PUZZLE_INPUTS_DIRECTORY / f'Day_{day:0>2}.txt').open() as input_file:
        for input_line in input_file:
            yield input_line.rstrip('\n')