from aoc2024 import utilities
from aoc2024.graph_theory import grid2d


def solve_part_one():
    pushed_bytes = '\n'.join(utilities.input_lines(day=18))

    memory_space = grid2d(71, 71)
    for pushed_byte in pushed_bytes.split('\n')[:1024]:
        grid_node = tuple(map(int, pushed_byte.split(',')))[::-1]
        memory_space.remove_node(grid_node)

    def taxicab(node1, node2):
        if len(node1) != len(node2):
            raise ValueError(
                f'Dimension mismatch between nodes {node1} and {node2}.'
            )
        return sum(
            abs(entry1 - entry2)
            for entry1, entry2 in zip(node1, node2)
        )

    paths, distance = memory_space.shortest_path_astar(
        source=(0, 0), target=(70, 70), heuristic=taxicab, edge_weight=1
    )
    return distance


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())