from __future__ import annotations

import pytest

from aoc2024.pathfinding import Direction


class TestDirection:
    def test_from_caret_constructs_direction_from_caret_symbol(self):
        expected_caret_direction = {
            '^': Direction.UP,
            'v': Direction.DOWN,
            '<': Direction.LEFT,
            '>': Direction.RIGHT
        }
        for caret, expected_direction in expected_caret_direction.items():
            assert Direction.from_caret(caret) is expected_direction

    def test_from_caret_raises_error_for_noncaret_inputs(self):
        with pytest.raises(ValueError):
            Direction.from_caret(')')

    def test_to_caret_is_the_right_inverse_of_from_caret(self):
        for direction in Direction:
            assert Direction.from_caret(direction.to_caret()) is direction