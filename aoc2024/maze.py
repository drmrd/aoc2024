from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from copy import deepcopy
from enum import Enum
from functools import partial
from typing import Union

from aoc2024.graph_theory import DiGraph
from aoc2024.pathfinding import Direction
from aoc2024.vector import Vector, taxicab

type Position = tuple[int, int]
type OrientedPosition = tuple[Position, Direction]


class Component(str, Enum):
    WALL = '#'
    FREE = '.'
    START = 'S'
    END = 'E'


class Maze[PositionType: Position | OrientedPosition]:
    def __init__(
            self,
            graph: DiGraph[PositionType],
            start: PositionType,
            ends: Sequence[PositionType],
            oriented: bool = True
    ):
        self._graph = graph
        self._start = start
        self._ends = set(ends)
        self._oriented_nodes = oriented

    @property
    def start(self) -> PositionType:
        return self._start

    @property
    def ends(self) -> set[PositionType]:
        return self._ends

    def find_all_cheapest_paths(self):
        return {
            end: self._graph.all_shortest_paths(self._start, end)
            for end in self._ends
        }

    def find_cheapest_path(self):
        if isinstance(self.start[0], tuple):
            def heuristic(node1, node2):
                return taxicab(node1[0], node2[0])
        else:
            heuristic = taxicab
        return min(
            (
                self._graph.shortest_path(
                    source=self._start,
                    target=end,
                    heuristic=heuristic
                )
                for end in self.ends
            ),
            key=lambda path_and_cost: path_and_cost[1]
        )

    def find_cheapest_paths_astar(self):
        if isinstance(self.start[0], tuple):
            def heuristic(node1, node2):
                return taxicab(node1[0], node2[0])
        else:
            heuristic = taxicab
        return {
            end: self._graph.shortest_path(
                self._start, end,
                heuristic=heuristic
            )
            for end in self._ends
        }

    def to_graph(self) -> DiGraph[PositionType]:
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

        edges: deque[tuple[PositionType, PositionType]] = deque()
        start: PositionType | None = None
        ends: deque[PositionType] = deque()
        for position, entry in parsed_passable_position.items():
            if entry is Component.START:
                if start is not None:
                    raise NotImplementedError(
                        'Multiple starting locations are not supported.'
                    )
                start = create_node(position, start_direction)  # type: ignore
            for direction in Direction:
                if entry is Component.END:
                    ends.append(create_node(position, direction))  # type: ignore
                if oriented_nodes:
                    edges.append(
                        create_edge(  # type: ignore
                            position, direction,
                            position, direction.rotate_clockwise(),
                            cost_rotate, oriented=oriented_nodes
                        )
                    )
                    edges.append(
                        create_edge(  # type: ignore
                            position, direction,
                            position, direction.rotate_counterclockwise(),
                            cost_rotate, oriented=oriented_nodes
                        )
                    )
                neighbor = tuple(Vector(*position) + direction.grid_vector)
                if neighbor in parsed_passable_position:
                    edges.append(
                        create_edge(  # type: ignore
                            position, direction,
                            neighbor, direction,
                            cost_move_forward, oriented=oriented_nodes
                        )
                    )

        maze_graph = DiGraph(*edges)
        return cls(
            graph=maze_graph,
            start=start,  # type: ignore
            ends=ends,
            oriented=oriented_nodes
        )

    @staticmethod
    def create_node(
            position: Position,
            direction: Direction | None,
            oriented: bool = False
    ) -> Position | OrientedPosition:
        if oriented and direction is None:
            raise ValueError(
                'A direction must be provided to create an oriented node.'
            )
        return (position, direction) if oriented else position  # type: ignore

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