from aoc2024 import utilities
from aoc2024.maze import Maze


def solve_part_one():
    return min(
        score
        for _, score in Maze.from_map(
            '\n'.join(utilities.input_lines(day=16)), oriented_nodes=True
        ).find_cheapest_paths().values()
    )


def solve_part_two():
    best_paths = Maze.from_map(
        '\n'.join(utilities.input_lines(day=16)),
        oriented_nodes=True
    ).find_cheapest_paths().values()
    best_score = min(score for _, score in best_paths)
    best_path_positions = {
        position
        for paths, score in best_paths
        for path in paths
        for position, _ in path
        if score == best_score
    }
    return len(best_path_positions)


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())