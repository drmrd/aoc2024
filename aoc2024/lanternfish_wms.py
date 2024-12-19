from __future__ import annotations

import itertools
from collections import deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from enum import Enum
from functools import cached_property, lru_cache
from typing import ClassVar, Type

from aoc2024.vector import Vector


class MovingTheImmovable(ValueError):
    pass


class Direction(Enum):
    UP = -1
    DOWN = 1
    LEFT = -1j
    RIGHT = 1j

    @cached_property
    def grid_offsets(self) -> tuple[int, int]:
        return int(self.value.real), int(self.value.imag)

    @cached_property
    def grid_vector(self) -> Vector[int]:
        return Vector(*self.grid_offsets)

    @lru_cache(4)
    def rotate_counterclockwise(self) -> Direction:
        return Direction(self.value * 1j)

    @lru_cache(4)
    def rotate_clockwise(self) -> Direction:
        return Direction(self.value * -1j)

    @classmethod
    @lru_cache(16)
    def from_caret(cls, caret: str) -> Direction:
        try:
            return {
                '^': cls.UP, 'v': cls.DOWN, '<': cls.LEFT, '>': cls.RIGHT
            }[caret]
        except KeyError:
            raise ValueError(f'Unknown direction caret "{caret}".')


@dataclass
class Entity:
    movable: ClassVar[bool]
    map_string: ClassVar[str]
    warehouse: Warehouse
    footprint: list[Vector[int]]

    def __str__(self):
        return self.__class__.map_string

    @property
    def left_edge(self) -> Vector[int]:
        return self.footprint[0]

    def can_move(self, direction: Direction) -> bool:
        neighbors = self.get_neighbors(direction)
        return self.__class__.movable and all(
            neighbor is None or neighbor.can_move(direction)
            for neighbor in neighbors
        )

    def move(self, direction: Direction, first_mover=True):
        neighbors = [
            neighbor for neighbor in self.get_neighbors(direction)
            if neighbor is not None
        ]
        if all(neighbor.can_move(direction) for neighbor in neighbors):
            for neighbor in neighbors:
                neighbor.move(direction, first_mover=False)
        else:
            return
                # try:
                # except MovingTheImmovable as error:
                #     if first_mover:
                #         if neighbors:
                #             continue
                #         else:
                #             return
                #     else:
                #         raise error
        new_footprint = [
            position + direction.grid_vector for position in self.footprint
        ]
        freed_positions = [
            position
            for position in self.footprint
            if position not in new_footprint
        ]
        for row, column in freed_positions:
            self.warehouse.grid[row][column] = None
        self.footprint = new_footprint
        for row, column in self.footprint:
            self.warehouse.grid[row][column] = self

    def get_neighbors(self, direction: Direction) -> list[Entity | None]:
        neighbors = [
            self.warehouse.grid[neighbor_position[0]][neighbor_position[1]]
            for position in self.footprint
            if (
                0 <= (neighbor_position := position + direction.grid_vector)[0]
                  < self.warehouse.shape[0]
            ) and (
                0 <= neighbor_position[1] < self.warehouse.shape[1]
            ) and neighbor_position not in self.footprint
        ]

        try:
            neighbor1, neighbor2 = neighbors
        except ValueError:
            return neighbors

        if neighbor1 is neighbor2:
            neighbors = [neighbor1]
        return neighbors


@dataclass
class Wall(Entity):
    movable = False
    map_string = '#'


@dataclass
class Box(Entity):
    movable = True
    map_string = 'O'

    @property
    def gps_coordinate(self) -> int:
        row, column = next(iter(self.footprint))
        return 100 * row + column


@dataclass
class DummyThiccWall(Entity):
    movable = False
    map_string = '##'


@dataclass
class DummyThiccBox(Entity):
    movable = True
    map_string = '[]'

    @property
    def gps_coordinate(self) -> int:
        row, left_column = self.left_edge
        return 100 * row + left_column


@dataclass
class RoeBot(Entity):
    movable = True
    map_string = '@'
    routine: Iterator[Direction]


@dataclass
class Warehouse:
    grid: list[list[Entity | None]]
    shape: tuple[int, int]
    roe_bot: RoeBot | None

    def to_lanternfish_map(self) -> str:
        map_ = [['.' for column in row] for row in self.grid]
        for row in range(self.shape[0]):
            for column in range(self.shape[1]):
                if (
                        map_[row][column] != '.'
                        or self.grid[row][column] is None
                ):
                    continue
                entity = self.grid[row][column]
                for index, character in enumerate(entity.map_string):
                    map_row, map_column = entity.footprint[index]
                    map_[map_row][map_column] = entity.map_string[index]
        return '\n'.join(''.join(row) for row in map_)

    @classmethod
    def from_lanternfish_printout(
            cls,
            map_: list[str],
            roe_bot_routine: str,
            passive_entity_types: Sequence[Type[Entity]] = (Wall, Box),
            dummy_thiccen: bool = False
    ) -> Warehouse:
        if dummy_thiccen:
            map_ = _apply_dummy_thiccener(map_)

        shape = rows, columns = len(map_), len(map_[0])
        warehouse = cls(
            grid=[[None for _ in range(columns)] for _ in range(rows)],
            shape=shape,
            roe_bot=None
        )

        parsed_roe_bot_routine = (
            Direction.from_caret(caret)
            for caret in ''.join(roe_bot_routine.split('\n'))
        )

        map_string_width = {
            entity_type: len(entity_type.map_string)
            for entity_type in passive_entity_types
        }
        # Note this does not meaningfully affect the order of the provided
        # entity types for parsing purposes, since `sorted' is a stable sorting
        # algorithm.
        passive_entity_types = sorted(
            passive_entity_types,
            key=lambda type_: -map_string_width[type_]
        )

        grid_positions = itertools.product(*map(range, shape))
        while grid_positions:
            try:
                row, column = next(grid_positions)
            except StopIteration:
                break

            entity = None
            for entity_type in passive_entity_types:
                entity_string_width = map_string_width[entity_type]
                if column + entity_string_width > columns:
                    continue
                entity_columns = slice(column, column + entity_string_width)
                if map_[row][entity_columns] == entity_type.map_string:
                    entity = entity_type(
                        warehouse,
                        [
                            Vector(row, entity_column)
                            for entity_column in range(
                                *entity_columns.indices(columns)
                            )
                        ]
                    )
                    warehouse.grid[row][entity_columns] = itertools.repeat(entity, entity_string_width)
                    for _ in range(entity_string_width - 1):
                        next(grid_positions)
                    break
            else:
                if map_[row][column] == RoeBot.map_string:
                    entity = RoeBot(
                        warehouse,
                        [Vector(row, column)],
                        parsed_roe_bot_routine
                    )
                    warehouse.grid[row][column] = entity
                elif map_[row][column] != '.':
                    raise ValueError(
                        f'Parsing error at map position {(row, column)} '
                        f'(character "{map_[row][column]}").'
                    )

            if isinstance(entity, RoeBot):
                warehouse.roe_bot = entity

        return warehouse

def _apply_dummy_thiccener(
        map_: list[str],
        thiccened_map_strings: tuple[tuple[str, str]] = (
            (Wall.map_string, DummyThiccWall.map_string),
            (Box.map_string, DummyThiccBox.map_string)
        )
) -> list[str]:
    thiccened_string = {
        '.': '..',
        RoeBot.map_string: f'{RoeBot.map_string}.',
        **dict(thiccened_map_strings)
    }

    def thiccen_row(row) -> str:
        proto_thicc_row = deque()
        column_index = 0
        while column_index < len(row):
            for unthicc, thicc in thiccened_string.items():
                if row[column_index:column_index + len(unthicc)] == unthicc:
                    proto_thicc_row.append(thicc)
                    column_index += len(unthicc)
                    break
            else:
                column_index += 1
        return ''.join(proto_thicc_row)

    dummy_thicc_map = [thiccen_row(row) for row in map_]
    enumerated_thicc_rows = iter(enumerate(dummy_thicc_map))
    thicc_row_length = len(next(enumerated_thicc_rows)[1])
    for index, thicc_row in enumerated_thicc_rows:
        if (other_thicc_row_length := len(thicc_row)) != thicc_row_length:
            raise ValueError(
                f'Thiccened rows 0 and {index} have different lengths '
                f'({thicc_row_length} and {other_thicc_row_length}, '
                'respectively.)'
            )

    return dummy_thicc_map