from __future__ import annotations

import itertools
import math
import re
from collections import deque
from functools import cache

from aoc2024 import utilities
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
        layout_shape = len(layout_rows), len(layout_rows[0])

        physical_transitions = deque()
        key_position = {}
        for row_index, column_index in itertools.product(*map(range, layout_shape)):
            key_value = layout_rows[row_index][column_index]
            if layout_rows[row_index][column_index] == ' ':
                continue
            key = Vector(row_index, column_index)
            key_position[key_value] = tuple(key)
            for direction in Direction:
                neighbor = key + direction.grid_vector
                if (
                        min(neighbor) >= 0
                        and neighbor[0] < layout_shape[0]
                        and neighbor[1] < layout_shape[1]
                        and (
                            value := layout_rows[neighbor[0]][neighbor[1]]
                        ) != ' '
                ):
                    physical_transitions.append(
                        (tuple(key), tuple(neighbor), {'direction': direction})
                    )

        for index, row in enumerate(layout_rows):
            try:
                self._current_position = index, row.index(start_position)
                break
            except ValueError:
                continue
        else:
            raise ValueError(
                f'No key with value "{start_position}" found in layout.'
            )
        self._key_graph = DiGraph(*physical_transitions)
        self._key_position = key_position

    def shortest_paths(self, start, stop):
        paths, length = self._key_graph.all_shortest_paths(
            self._key_position[start],
            self._key_position[stop],
            edge_weight=1
        )
        if not paths:
            raise ValueError(f'No paths found from "{start}" to "{stop}".')
        return {
            'position_paths': paths,
            'movement_paths': [
                [
                    self._key_graph[edge]['direction'].to_caret()
                    for edge in itertools.pairwise(path)
                ]
                for path in paths
            ],
            'length': length
        }

    @cache
    def to_position(self, key: str) -> tuple[int, int]:
        return self._key_position[key]  # type: ignore

    @cache
    def to_key(self, position: tuple[int, int] | Vector[int]) -> tuple[int, int]:
        position = tuple(position)
        for key, key_position in self._key_position.items():
            if key_position == position:
                return key
        raise ValueError(f'No key found at position {position}')

    def path_to_key_presses(self, path: str) -> str:
        current_position = self._key_position['A']
        key_presses = deque()
        for action in path:
            if action == 'A':
                key_presses.append(self.to_key(current_position))
                continue
            current_position = tuple(
                Vector(*current_position) + Direction.from_caret(action).grid_vector
            )
        return ''.join(key_presses)


def door_keypad_sequence(door_code: str | list[str]) -> list[str]:
    door_keypad = Keypad(
        '\n'.join([
            '789',
            '456',
            '123',
            ' 0A'
        ])
    )
    if isinstance(door_code, str):
        door_code = [door_code]
    return keypad_controller_movement_paths(door_keypad, door_code)


def directional_keypad_sequence(directions: str | list[str]) -> list[str]:
    directional_keypad = Keypad(
        '\n'.join([
            ' ^A',
            '<v>'
        ])
    )
    if isinstance(directions, str):
        directions = [directions]
    return keypad_controller_movement_paths(directional_keypad, directions)


def keypad_controller_movement_paths(keypad, keypad_button_sequences: list[str]) -> list[str]:
    movement_paths = deque()
    for keypad_button_sequence in keypad_button_sequences:
        interkey_paths = deque()
        source = 'A'
        for target in keypad_button_sequence:
            paths_from_source_to_target = keypad.shortest_paths(
                source, target
            )['movement_paths']
            interkey_paths.append(paths_from_source_to_target)
            source = target
        movement_paths.extend(
            ''.join(f'{''.join(key_pair_path)}A' for key_pair_path in interkey_path)
            for interkey_path in itertools.product(*interkey_paths)
        )
    return list(movement_paths)


def find_minimal_robot_robot_robot_control_sequences(
        door_code: str
) -> str:
    door_keypad_robot_sequences = door_keypad_sequence(door_code)
    minimal_door_keypad_sequence_length = len(
        shortest_sequence(door_keypad_robot_sequences)
    )
    first_directional_keypad_robot_sequences = directional_keypad_sequence([
        sequence
        for sequence in door_keypad_robot_sequences
        if len(sequence) == minimal_door_keypad_sequence_length
    ])
    minimal_first_directional_keypad_robot_sequence_length = len(
        shortest_sequence(first_directional_keypad_robot_sequences)
    )
    second_directional_keypad_robot_sequences = directional_keypad_sequence([
        sequence
        for sequence in first_directional_keypad_robot_sequences
        if len(sequence) == minimal_first_directional_keypad_robot_sequence_length
    ])
    return shortest_sequence(second_directional_keypad_robot_sequences)


def shortest_sequence(sequences: list[str]) -> str:
    current_minimal_sequence = None
    current_minimal_length = math.inf
    for sequence in sequences:
        if (sequence_length := len(sequence)) < current_minimal_length:
            current_minimal_sequence = sequence
            current_minimal_length = sequence_length
    return current_minimal_sequence


def complexity(code: str) -> int:
    return (
        int(re.sub(r'^(\d+).*$', r'\1', code))
        * len(find_minimal_robot_robot_robot_control_sequences(code))
    )


def solve_part_one():
    return sum(complexity(code) for code in utilities.input_lines(day=21))


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())