import timeit
from collections import deque

from aoc2024 import utilities


def solve_part_one():
    topographical_map = [
        list(map(int, line))
        for line in utilities.input_lines(day=10)
    ]
    map_shape = len(topographical_map), len(topographical_map[0])
    trailheads = [
        (row, column)
        for row in range(map_shape[0])
        for column in range(map_shape[1])
        if topographical_map[row][column] == 0
    ]

    trailhead_scores = 0
    for trailhead in trailheads:
        visited = set()
        to_visit = deque([trailhead])
        while to_visit:
            node = to_visit.pop()
            node_height = topographical_map[node[0]][node[1]]
            visited.add(node)
            to_visit.extend((
                neighbor
                for neighbor in _neighbors_at_height(
                    topographical_map, node, node_height + 1, map_shape
                )
                if neighbor not in visited
            ))
        trailhead_scores += len({
            node for node in visited
            if topographical_map[node[0]][node[1]] == 9
        })
    return trailhead_scores


def solve_part_two():
    return 'TBD'


def _neighbors_at_height(map, node, height, map_shape):
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    row, column = node
    for row_offset, column_offset in neighbor_offsets:
        neighbor_row = row + row_offset
        neighbor_column = column + column_offset
        if (
                (neighbor := (neighbor_row, neighbor_column)) != (row, column)
                and 0 <= neighbor_row < map_shape[0]
                and 0 <= neighbor_column < map_shape[1]
                and map[neighbor_row][neighbor_column] == height
        ):
            yield neighbor


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())

    executions, repetitions = 100, 10
    print(
        '\n=*=*=*= Best Times =*=*=*=',
        f'({repetitions} repetitions of {executions} executions)'
    )
    print(
        'Part 1:',
        min(
            timeit.timeit(solve_part_one, number=executions) / executions
            for _ in range(repetitions)
        )
    )
    print('Part 2:', 'TBD')