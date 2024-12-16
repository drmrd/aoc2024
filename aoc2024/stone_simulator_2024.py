import itertools
from collections.abc import Iterable, Iterator


class StoneSimulator2024:
    def __init__(self, stones: Iterable[int]):
        self._stones = iter(stones)

    def blink(self):
        return StoneSimulator2024(
            itertools.chain.from_iterable(
                self._transformed_stone_iter(stone)
                for stone in self
            )
        )

    def __iter__(self):
        self._stones, iterator = itertools.tee(self._stones)
        return iterator

    def _transformed_stone_iter(self, stone) -> Iterator[int]:
        if stone == 0:
            yield 1
        elif (digits := len(stone_string := str(stone))) % 2 == 0:
            yield from map(
                int, (stone_string[:digits // 2], stone_string[digits // 2:])
            )
        else:
            yield 2024 * stone