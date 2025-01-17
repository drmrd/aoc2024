from __future__ import annotations

import itertools
import math

from aoc2024.pathfinding import Direction
from aoc2024.vector import Vector

type Plot = tuple[int, int]
type Region = frozenset[Plot]


def garden_regions(garden: dict[Plot, str]) -> set[Region]:
    *_, final_indices = garden
    garden_shape = (final_indices[0] + 1, final_indices[1] + 1)
    region = {
        point: {point}
        for point in itertools.product(*map(range, garden_shape))
    }
    for point in itertools.product(*map(range, garden_shape)):
        neighbors_in_region = [
            neighbor
            for neighbor in _neighbors(point, garden_shape, ('up', 'left'))
            if garden[point] == garden[neighbor]  # type: ignore
        ]
        for neighbor in neighbors_in_region:
            region[point] |= region[neighbor]
        for regionmate in region[point] - {point}:
            region[regionmate] = region[point]
    return set(map(frozenset, region.values()))  # type: ignore


def area(region: Region) -> int:
    return len(region)


def edges(region: Region) -> int:
    region_vectors = {Vector(*plot) for plot in region}
    cardinal_directions = [Vector(*direction.grid_offsets) for direction in Direction]
    boundary_edge_segments = {
        (plot, direction)
        for plot in region_vectors
        for direction in cardinal_directions
        if plot + direction not in region_vectors
    }
    boundary_edge_representatives = boundary_edge_segments - {
        (
            plot + Vector(
                *Direction(
                    complex(*(direction))
                ).rotate_clockwise().grid_offsets
            ),
            direction
        )
        for plot, direction in boundary_edge_segments
    }
    return len(boundary_edge_representatives)


def perimeter(region: Region) -> int:
    return sum(_plot_perimeter(plot, region) for plot in region)


def fence_cost(garden: dict[Plot, str], bulk_discount=False) -> int:
    length_function = edges if bulk_discount else perimeter
    return sum(
        area(region) * length_function(region)
        for region in garden_regions(garden)
    )


def _plot_perimeter(plot: Plot, region: Region) -> int:
    return 4 - len(region & set(_neighbors(plot)))


def _neighbors(
        node,
        grid_shape=(math.inf, math.inf),
        directions=('up', 'down', 'left', 'right')
):
    neighbor_offsets = {
        'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)
    }
    selected_offsets = (
        neighbor_offsets[direction] for direction in directions
    )
    row, column = node
    for row_offset, column_offset in selected_offsets:
        neighbor_row = row + row_offset
        neighbor_column = column + column_offset
        if (
                0 <= neighbor_row < grid_shape[0]
                and 0 <= neighbor_column < grid_shape[1]
        ):
            yield neighbor_row, neighbor_column