from aoc2024.maze import Maze


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
    maze = Maze.from_map(unparsed_maze)

    best_paths = maze.find_best_paths()

    assert min(score for _, score in best_paths.values()) == 7036


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
    maze = Maze.from_map(unparsed_maze)

    best_paths = maze.find_best_paths().values()
    best_score = min(score for _, score in best_paths)
    best_path_positions = {
        position
        for paths, score in best_paths
        for path in paths
        for position, _ in path
        if score == best_score
    }

    assert len(best_path_positions) == 45


def test_day16_part2_example1():
    pushed_bytes = '\n'.join([
        '5,4', '4,2', '4,5', '3,0', '2,1', '6,3', '2,4', '1,5', '0,6', '3,3',
        '2,6', '5,1', '1,2', '5,5', '2,5', '6,5', '1,4', '0,4', '6,4', '1,1',
        '6,1', '1,0', '0,5', '1,6', '2,0'
    ])

    maze = Maze.from_map(unparsed_maze)

    best_paths = maze.find_best_paths().values()
    best_score = min(score for _, score in best_paths)
    best_path_positions = {
        position
        for paths, score in best_paths
        for path in paths
        for position, _ in path
        if score == best_score
    }

    assert len(best_path_positions) == 45