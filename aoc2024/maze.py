from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from enum import Enum

from aoc2024.graph_theory import Graph
from aoc2024.pathfinding import Direction
from aoc2024.vector import Vector

type Position = tuple[int, int]
type OrientedPosition = tuple[Position, Direction]


class Component(str, Enum):
    WALL = '#'
    FREE = '.'
    START = 'S'
    END = 'E'


class Maze:
    def __init__(
            self,
            graph: Graph[OrientedPosition],
            start: OrientedPosition,
            ends: Sequence[OrientedPosition]
    ):
        self._graph = graph
        self._start = start
        self._ends = set(ends)

    def find_best_paths(self):
        return {
            end: self._graph.shortest_path(self._start, end)
            for end in self._ends
        }

    @classmethod
    def from_map(cls, maze_map: str) -> Maze:
        parsed_passable_position = {
            (row, column): parsed_entry
            for row, map_row in enumerate(maze_map.split('\n'))
            for column, map_entry in enumerate(map_row)
            if (parsed_entry := Component(map_entry)) is not Component.WALL
        }
        oriented_edges = deque()
        start = None
        ends = deque()
        for position, entry in parsed_passable_position.items():
            if entry is Component.START:
                if start is not None:
                    raise NotImplementedError(
                        'Multiple starting locations are not supported.'
                    )
                start = (position, Direction.RIGHT)
            for direction in (Direction.DOWN, Direction.RIGHT):
                if entry is Component.END:
                    ends.append((position, direction))
                oriented_edges.append(
                    (
                        (position, direction),
                        (position, direction.rotate_clockwise()),
                        1000
                    )
                )
                neighbor = tuple(Vector(*position) + direction.grid_vector)
                if neighbor in parsed_passable_position:
                    oriented_edges.append(
                        ((position, direction), (neighbor, direction), 1)
                    )

        maze_graph = Graph(*oriented_edges)
        return cls(
            graph=maze_graph,
            start=start,
            ends=ends
        )