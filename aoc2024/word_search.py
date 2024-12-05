import collections
import itertools
from collections.abc import Iterable, Iterator


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