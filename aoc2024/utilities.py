from collections.abc import Generator
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
PUZZLE_INPUTS_DIRECTORY: Path = REPO_ROOT / 'puzzle_inputs'


def input_grid(
        day: int, *, rowsep=None, colsep='', caster=None
) -> list[list]:
    if caster is None:
        caster = lambda x: x

    if rowsep is None:
        lines = input_lines(day)
    else:
        read_text_kwargs = {
            'newline': (
                rowsep if rowsep in {None, '', '\r', '\n', '\r\n'} else ''
            )
        }
        lines = (
            (PUZZLE_INPUTS_DIRECTORY / f'Day_{day:0>2}.txt')
                    .read_text(**read_text_kwargs)
                    .split(rowsep)
        )

    if colsep != '':
        splitter = lambda line: line.split(colsep)
    else:
        splitter = list

    return [[caster(entry) for entry in splitter(line)] for line in lines]


def input_lines(day: int) -> Generator[str]:
    with (PUZZLE_INPUTS_DIRECTORY / f'Day_{day:0>2}.txt').open() as input_file:
        for input_line in input_file:
            yield input_line.rstrip('\n')