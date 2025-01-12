from collections.abc import Generator, Iterable
from pathlib import Path

import aocd

REPO_ROOT = Path(__file__).parent.parent
PUZZLE_INPUTS_DIRECTORY: Path = REPO_ROOT / 'puzzle_inputs'


def input_grid(
        year: int, day: int, *, rowsep=None, colsep='', caster=None
) -> list[list]:
    if caster is None:
        caster = lambda x: x

    if rowsep is None:
        lines: Iterable = input_lines(year, day)
    else:
        read_text_kwargs = {
            'newline': (
                rowsep if rowsep in {None, '', '\r', '\n', '\r\n'} else ''
            )
        }
        lines = aocd.get_data(year=year, day=day).split(rowsep)

    if colsep != '':
        splitter = lambda line: line.split(colsep)
    else:
        splitter = list

    return [[caster(entry) for entry in splitter(line)] for line in lines]


def input_lines(year: int, day: int) -> Generator[str]:
    data = aocd.get_data(year=year, day=day)
    for input_line in data.split('\n'):
        yield input_line.rstrip('\n')