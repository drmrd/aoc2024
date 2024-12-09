from collections.abc import Generator
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
PUZZLE_INPUTS_DIRECTORY: Path = REPO_ROOT / 'puzzle_inputs'


def input_lines(day: int) -> Generator[str]:
    with (PUZZLE_INPUTS_DIRECTORY / f'Day_{day:0>2}.txt').open() as input_file:
        for input_line in input_file:
            yield input_line.rstrip('\n')