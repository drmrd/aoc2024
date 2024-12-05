import collections
import itertools
from collections.abc import Iterable, Iterator


def cross_count(puzzle: str) -> int:
    def cross_indices(puzzle: str) -> Iterator[tuple[int, int]]:
        puzzle_rows = puzzle.split('\n')
        cross_patterns = {'MMASS', 'SMASM', 'SSAMM', 'MSAMS'}
        for window_row_start_index in range(len(puzzle_rows) - 2):
            for window_column_start_index in range(len(puzzle_rows[0]) - 2):
                cross_candidate = ''.join([
                    puzzle_rows[window_row_start_index][window_column_start_index],
                    puzzle_rows[window_row_start_index][window_column_start_index + 2],
                    puzzle_rows[window_row_start_index + 1][window_column_start_index + 1],
                    puzzle_rows[window_row_start_index + 2][window_column_start_index],
                    puzzle_rows[window_row_start_index + 2][window_column_start_index + 2]
                ])
                if cross_candidate in cross_patterns:
                    yield window_row_start_index, window_column_start_index
    return len(list(cross_indices(puzzle)))


def count(puzzle: str, words: Iterable[str]) -> int:
    return (
        _count_in_rows(puzzle, words)
        + _count_in_columns(puzzle, words)
        + _count_on_diagonals(puzzle, words)
    )


def _count_in_strings(
        strings: Iterable,
        words: Iterable[str]
) -> int:
    return sum(
        word == candidate
        for word_length, word_group in itertools.groupby(sorted(words, key=len), key=len)
        for word in word_group
        for string in itertools.chain(strings, map(reversed, strings))
        for candidate in _sliding_word(string, word_length)
    )


def _count_in_rows(puzzle: str, words: Iterable[str]) -> int:
    rows = puzzle.split('\n')
    return _count_in_strings(rows, words)


def _count_in_columns(puzzle: str, words: Iterable[str]) -> int:
    columns = list(zip(*puzzle.split('\n')))
    return _count_in_strings(columns, words)


def _count_on_diagonals(puzzle: str, words: Iterable[str]) -> int:
    rows = puzzle.split('\n')
    reversed_rows = list(reversed(rows))

    row_count = len(rows)
    column_count = len(rows[0])
    diagonal_count = row_count + column_count - 1
    diagonals = [
        ''.join(
            directed_rows[row_index][column_index]
            for row_index in range(diagonal_index + 1)
            if (
                row_index < row_count
                and (
                    column_index := diagonal_index - row_index
                ) < column_count
            )
        )
        for directed_rows in [rows, reversed_rows]
        for diagonal_index in range(diagonal_count)
    ]
    return _count_in_strings(diagonals, words)


def _sliding_word(text, word_length: int) -> Iterator:
    word = collections.deque(itertools.islice(text, word_length - 1), maxlen=word_length)
    for x in text:
        word.append(x)
        yield ''.join(word)