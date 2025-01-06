from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from copy import deepcopy
from enum import Enum
from functools import partial
from typing import Union

from aoc2024.graph_theory import UndirectedGraph
from aoc2024.pathfinding import Direction
from aoc2024.vector import Vector, taxicab

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
            graph: UndirectedGraph[OrientedPosition],
            start: OrientedPosition,
            ends: Sequence[OrientedPosition]
    ):
        self._graph = graph
        self._start = start
        self._ends = set(ends)

    @property
    def start(self) -> Position | OrientedPosition:
        return self._start

    @property
    def ends(self) -> set[Position] | set[OrientedPosition]:
        return self._ends

    def find_cheapest_paths(self):
        return {
            end: self._graph.all_shortest_paths(self._start, end)
            for end in self._ends
        }

    def find_cheapest_paths_astar(self):
        if isinstance(self.start[0], tuple):
            def heuristic(node1, node2):
                return taxicab(node1[0], node2[0])
        else:
            heuristic = taxicab
        return {
            end: self._graph.shortest_path_astar(
                self._start, end,
                heuristic=heuristic
            )
            for end in self._ends
        }

    def to_graph(self) -> UndirectedGraph[Position] | UndirectedGraph[OrientedPosition]:
        return deepcopy(self._graph)

    @classmethod
    def from_map(
            cls,
            maze_map: str,
            oriented_nodes: bool = False,
            cost_move_forward: float = 1,
            cost_rotate: float = 1000,
            start_direction: Direction | None = None
    ) -> Maze:
        parsed_passable_position = {
            (row, column): parsed_entry
            for row, map_row in enumerate(maze_map.split('\n'))
            for column, map_entry in enumerate(map_row)
            if (parsed_entry := Component(map_entry)) is not Component.WALL
        }
        if oriented_nodes and start_direction is None:
            raise ValueError(
                'Requested a maze with orientation-tracking (oriented_nodes '
                'is True) without providing a starting point direction via '
                'start_direction.'
            )
        create_node = partial(Maze.create_node, oriented=oriented_nodes)
        create_edge = partial(Maze.create_edge, oriented=oriented_nodes)

        edges = deque()
        start = None
        ends = deque()
        for position, entry in parsed_passable_position.items():
            if entry is Component.START:
                if start is not None:
                    raise NotImplementedError(
                        'Multiple starting locations are not supported.'
                    )
                start = create_node(position, start_direction)
            for direction in (Direction.DOWN, Direction.RIGHT):
                if entry is Component.END:
                    ends.append(create_node(position, direction))
                if oriented_nodes:
                    edges.append(
                        create_edge(
                            position, direction,
                            position, direction.rotate_clockwise(),
                            cost_rotate
                        )
                    )
                neighbor = tuple(Vector(*position) + direction.grid_vector)
                if neighbor in parsed_passable_position:
                    edges.append(
                        create_edge(
                            position, direction,
                            neighbor, direction,
                            cost_move_forward
                        )
                    )

        maze_graph = UndirectedGraph(*edges)
        return cls(
            graph=maze_graph,
            start=start,
            ends=ends
        )

    @staticmethod
    def create_node(
            position: Position, direction: Direction, oriented: bool = False
    ) -> Position | OrientedPosition:
        return (position, direction) if oriented else position

    @staticmethod
    def create_edge(
            position1, direction1, position2, direction2, weight, oriented: bool = False
    ) -> Union[
        tuple[Position, Position, float],
        tuple[OrientedPosition, OrientedPosition, float]
    ]:
        if oriented:
            return (position1, direction1), (position2, direction2), weight
        else:
            return position1, position2, weight