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