import collections
import itertools
from collections.abc import Iterable, Iterator


def count(puzzle: str, words: Iterable[str]) -> int:
    return _count_in_rows(puzzle, words)


def _count_in_rows(puzzle: str, words: Iterable[str]) -> int:
    rows = puzzle.split('\n')
    return sum(
        word == candidate
        for word_length, word_group in itertools.groupby(sorted(words, key=len), key=len)
        for word in word_group
        for row in itertools.chain(rows, map(reversed, rows))
        for candidate in _sliding_word(row, word_length)
    )


def _sliding_word(text: str, word_length: int) -> Iterator:
    word = collections.deque(itertools.islice(text, word_length - 1), maxlen=word_length)
    for x in text:
        word.append(x)
        yield ''.join(word)