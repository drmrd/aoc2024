from __future__ import annotations

import itertools
from collections.abc import Iterator
from typing import Self

from aoc2024.pathfinding import Direction

type Position = tuple[int, int]


class GuardedLab:
    def __init__(
            self,
            initial_states
    ):
        self._shape = len(initial_states), len(initial_states[0])

        self._blocked = {
            (row, column)
            for row, column in itertools.product(*map(range, self._shape))
            if initial_states[row][column] == '#'
        }

        guard_states = {'v', '^', '<', '>'}
        if sum(bool(set(row) & guard_states) for row in initial_states) > 1:
            raise ValueError('Multiple guards are not supported.')

        self._is_guarded = False
        for row, column in itertools.product(*map(range, self._shape)):
            if (guard_state := initial_states[row][column]) in guard_states:
                self._is_guarded = True
                self._guard_position = row, column
                self._guard_orientation = Direction.from_caret(guard_state)
                self._visited_with_orientation = {
                    (self._guard_position, self._guard_orientation): True
                }
                self._visited_count = 1
                break

        self._guard_is_gone = False
        self._guard_has_looped = False

    def __iter__(self) -> Iterator[Self]:
        while not (self._guard_is_gone or self._guard_has_looped):
            self._step_or_turn_right()
            yield self

    @property
    def visited_count(self) -> int:
        return self._visited_count

    @property
    def visited(self) -> set[Position]:
        return {position for position, _ in self._visited_with_orientation}

    @property
    def blocked(self) -> set[Position]:
        return self._blocked

    @property
    def is_guarded(self) -> bool:
        return self._is_guarded

    @property
    def guard_is_looping(self) -> bool:
        return self._guard_has_looped

    @property
    def guard_position(self) -> Position:
        try:
            return self._guard_position
        except AttributeError:
            raise ValueError('This lab is unguarded!')

    @property
    def guard_orientation(self) -> Direction:
        try:
            return self._guard_orientation
        except AttributeError:
            raise ValueError('This lab is unguarded!')

    def reset(self):
        self._is_guarded = False
        del self._guard_position
        del self._guard_orientation
        del self._guard_is_gone
        del self._guard_has_looped
        self._visited_with_orientation = {}
        self._visited_count = 0

    def add_guard(self, position: Position, orientation: Direction):
        if self._is_guarded:
            raise ValueError('Lab can have only one guard at a time.')
        self._is_guarded = True
        self._guard_position = position
        self._guard_orientation = orientation
        self._guard_is_gone = self._guard_has_looped = False
        self._visited_with_orientation = {
            (position, orientation): True
        }
        self._visited_count = 1

    def block(self, position: Position):
        if position == self.guard_position:
            raise ValueError(f'Position {position} is occupied by the guard.')
        self._blocked.add(position)

    def unblock(self, position: Position):
        self._blocked.remove(position)

    def _step_or_turn_right(self) -> None:
        if not self._is_guarded:
            raise ValueError('This lab is unguarded!')
        y, x = self._guard_position
        dy, dx = self._guard_orientation.grid_offsets
        y_next, x_next = y + dy, x + dx

        self._guard_is_gone |= (
            (min(y_next, x_next) < 0)
            or (y_next >= self._shape[0])
            or (x_next >= self._shape[1])
        )
        if self._guard_is_gone:
            return

        if (y_next, x_next) in self._blocked:
            self._guard_orientation = self._guard_orientation.rotate_clockwise()
            self._visited_with_orientation[
                (self._guard_position, self._guard_orientation)
            ] = True
        else:
            self._guard_position = y_next, x_next
            self._guard_has_looped |= self._visited_with_orientation.get(
                (self._guard_position, self._guard_orientation), False
            )
            self._visited_count += not any(
                self._visited_with_orientation.get(
                    (self._guard_position, orientation), False
                )
                for orientation in Direction
            )
            self._visited_with_orientation[
                (self._guard_position, self._guard_orientation)
            ] = True