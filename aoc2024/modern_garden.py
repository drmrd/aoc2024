import itertools
from collections import deque


def garden_regions(garden: dict[tuple[int, int], str]) -> set[frozenset[tuple[int, int]]]:
    *_, final_indices = garden
    garden_shape = (final_indices[0] + 1, final_indices[1] + 1)
    regions = deque()
    region_id = {}
    next_region_id = 0
    for point in itertools.product(*map(range, garden_shape)):
        neighbors_in_region = [
            neighbor
            for neighbor in _neighbors(point, garden_shape, ('left', 'up'))
            if garden[point] == garden[neighbor]
        ]
        match neighbors_in_region:
            case []:
                regions.append({point})
                region_id[point] = next_region_id
                next_region_id += 1
            case [neighbor]:
                neighboring_region_id = region_id[neighbor]
                regions[neighboring_region_id].add(point)
                region_id[point] = neighboring_region_id
            case _:
                first_id, second_id = sorted(map(region_id.get, neighbors_in_region))
                regions[first_id] |= regions[second_id]
                regions[second_id] = regions[first_id]
                regions[first_id].add(point)
                region_id[point] = first_id
    return {frozenset(region) for region in regions}


def _neighbors(node, grid_shape, directions=('up', 'down', 'left', 'right')):
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
            yield (neighbor_row, neighbor_column)