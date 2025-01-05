import pytest

from aoc2024.maze import Maze
from aoc2024.pathfinding import Direction


def test_from_map_with_orientation_requires_a_start_orientation_parameter():
    unparsed_maze = '\n'.join(['S..', '..E'])
    with pytest.raises(
            ValueError, match=r'\boriented_nodes\b.*\bstart_direction\b'
    ):
        Maze.from_map(
            unparsed_maze,
            oriented_nodes=True
        )


def test_day16_part1_example1():
    unparsed_maze = '\n'.join([
        '###############',
        '#.......#....E#',
        '#.#.###.#.###.#',
        '#.....#.#...#.#',
        '#.###.#####.#.#',
        '#.#.#.......#.#',
        '#.#.#####.###.#',
        '#...........#.#',
        '###.#.#####.#.#',
        '#...#.....#.#.#',
        '#.#.#.###.#.#.#',
        '#.....#...#.#.#',
        '#.###.#.#.#.#.#',
        '#S..#.....#...#',
        '###############'
    ])
    maze = Maze.from_map(
        unparsed_maze, oriented_nodes=True, start_direction=Direction.RIGHT
    )

    best_paths = maze.find_cheapest_paths()

    assert min(score for _, score in best_paths.values()) == 7036


def test_find_cheapest_paths_astar_oriented_day16_part1_example1():
    unparsed_maze = '\n'.join([
        '###############',
        '#.......#....E#',
        '#.#.###.#.###.#',
        '#.....#.#...#.#',
        '#.###.#####.#.#',
        '#.#.#.......#.#',
        '#.#.#####.###.#',
        '#...........#.#',
        '###.#.#####.#.#',
        '#...#.....#.#.#',
        '#.#.#.###.#.#.#',
        '#.....#...#.#.#',
        '#.###.#.#.#.#.#',
        '#S..#.....#...#',
        '###############'
    ])
    maze = Maze.from_map(
        unparsed_maze, oriented_nodes=True, start_direction=Direction.RIGHT
    )

    best_paths = maze.find_cheapest_paths_astar()

    assert min(score for _, score in best_paths.values()) == 7036


def test_find_cheapest_paths_astar_unoriented_day16_part1_example1():
    unparsed_maze = '\n'.join([
        '###############',
        '#.......#....E#',
        '#.#.###.#.###.#',
        '#.....#.#...#.#',
        '#.###.#####.#.#',
        '#.#.#.......#.#',
        '#.#.#####.###.#',
        '#...........#.#',
        '###.#.#####.#.#',
        '#...#.....#.#.#',
        '#.#.#.###.#.#.#',
        '#.....#...#.#.#',
        '#.###.#.#.#.#.#',
        '#S..#.....#...#',
        '###############'
    ])
    maze = Maze.from_map(unparsed_maze, oriented_nodes=False)

    best_paths = maze.find_cheapest_paths_astar()

    assert min(score for _, score in best_paths.values()) == 28


def test_day16_part2_example1():
    unparsed_maze = '\n'.join([
        '###############',
        '#.......#....E#',
        '#.#.###.#.###.#',
        '#.....#.#...#.#',
        '#.###.#####.#.#',
        '#.#.#.......#.#',
        '#.#.#####.###.#',
        '#...........#.#',
        '###.#.#####.#.#',
        '#...#.....#.#.#',
        '#.#.#.###.#.#.#',
        '#.....#...#.#.#',
        '#.###.#.#.#.#.#',
        '#S..#.....#...#',
        '###############'
    ])
    maze = Maze.from_map(
        unparsed_maze, oriented_nodes=True, start_direction=Direction.RIGHT
    )

    best_paths = maze.find_cheapest_paths().values()
    best_score = min(score for _, score in best_paths)
    best_path_positions = {
        position
        for paths, score in best_paths
        for path in paths
        for position, _ in path
        if score == best_score
    }

    assert len(best_path_positions) == 45


def test_day20_part1_example1():
    unparsed_maze = '\n'.join([
        '###############',
        '#...#...#.....#',
        '#.#.#.#.#.###.#',
        '#S#...#.#.#...#',
        '#######.#.#.###',
        '#######.#.#...#',
        '#######.#.###.#',
        '###..E#...#...#',
        '###.#######.###',
        '#...###...#...#',
        '#.#####.#.###.#',
        '#.#...#.#.#...#',
        '#.#.#.#.#.#.###',
        '#...#...#...###',
        '###############'
    ])
    maze = Maze.from_map(unparsed_maze)
    grid = maze.to_graph()
    start = maze.start
    end = list(maze.ends)[0]

    best_paths = grid.shortest_path(start, end, with_distance=True, edge_weight=1)

    assert best_paths[1] == 84
