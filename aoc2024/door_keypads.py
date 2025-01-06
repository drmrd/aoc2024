from __future__ import annotations

import itertools
from collections import deque

from aoc2024.graph_theory import DiGraph
from aoc2024.pathfinding import Direction
from aoc2024.vector import Vector


class Keypad:
    def __init__(self, layout, start_position='A'):
        layout_rows = layout.split('\n')
        if len({len(row) for row in layout_rows}) != 1:
            raise ValueError(
                'All layout rows must be the same length. Use a single space '
                'to represent keyless locations.'
            )

        layout_columns = list(zip(*layout_rows))
        layout_shape = len(layout_rows), len(layout_columns)

        physical_transitions = deque()

        for row_index, column_index in itertools.product(*map(range, layout_shape)):
            if layout_rows[row_index][column_index] == ' ':
                continue
            key = Vector(row_index, column_index)
            for direction in Direction:
                neighbor = key + direction.grid_vector
                if (
                        min(neighbor) >= 0
                        and neighbor[0] < layout_shape[0]
                        and neighbor[1] < layout_shape[1]
                        and layout_rows[neighbor[0]][neighbor[1]] != ' '
                ):
                    physical_transitions.append(
                        (key, neighbor, {'direction': direction})
                    )

        for index, row in enumerate(layout_rows):
            try:
                self._current_position = Vector(
                    index, row.index(start_position)
                )
                break
            except ValueError:
                continue
        else:
            raise ValueError(
                f'No key with value "{start_position}" found in layout.'
            )
        self._layout_rows = layout_rows
        self._key_graph = DiGraph(*physical_transitions)


DoorKeypad = Keypad(
    '\n'.join([
        '789',
        '456',
        '123',
        ' 0A'
    ])
)
print(DoorKeypad._current_position)