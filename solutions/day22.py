import itertools
from collections import deque
from functools import lru_cache
from typing import Generator

from aoc2024 import utilities


@lru_cache(16777216)
def evolve(secret_number: int) -> int:
    secret_number = (secret_number ^ secret_number << 6) & 16777215
    secret_number = (secret_number ^ secret_number >> 5) & 16777215
    secret_number = (secret_number ^ secret_number << 11) & 16777215
    return secret_number


def secret_sequence(secret_number: int) -> Generator[int]:
    while True:
        yield secret_number
        secret_number = evolve(secret_number)


def tuplewise(iterable, n):
    entry_iterables = itertools.tee(iterable, n)
    for first_shift in range(1, n):
        for iterable in entry_iterables[first_shift:]:
            next(iterable)
    return zip(*entry_iterables)


def first_occurrences(items, list_):
    result = {}
    for item in items:
        try:
            result[item] = list_.index(item)
        except ValueError:
            continue
    return result


def solve_part_one():
    total = 0
    for secret_number in map(int, utilities.input_lines(day=22)):
        for _ in range(2000):
            secret_number = evolve(secret_number)
        total += secret_number
    return total


def solve_part_two():
    last_secret_digit_sequences = [
        [secret % 10 for secret in itertools.islice(
            secret_sequence(monkey_secret), 2000)]
        for monkey_secret in map(int, utilities.input_lines(day=22))
    ]
    first_differences = [
        [
            second - first
            for first, second in itertools.pairwise(last_secret_digit_sequence)
        ]
        for last_secret_digit_sequence in last_secret_digit_sequences
    ]
    all_difference_quadruples = set()
    last_digits_at_quadruples = deque()
    for last_secret_digit_sequence, differences in zip(
            last_secret_digit_sequences, first_differences
    ):
        last_digits = {}
        for index, quadruple in zip(
                range(4, len(differences)),
                tuplewise(differences, 4)
        ):
            if quadruple not in last_digits:
                all_difference_quadruples.add(quadruple)
                last_digits[quadruple] = last_secret_digit_sequence[index]
        last_digits_at_quadruples.append(last_digits)

    return max(
        sum(
            last_digit.get(quadruple, 0)
            for last_digit in last_digits_at_quadruples
        )
        for quadruple in all_difference_quadruples
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())