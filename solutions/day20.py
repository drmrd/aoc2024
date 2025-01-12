import itertools
from collections import deque

from tqdm import tqdm

from aoc2024 import utilities
from aoc2024.maze import Maze
from aoc2024.vector import taxicab


def solve_part_one():
    maze = Maze.from_map(
        '\n'.join(utilities.input_lines(year=2024, day=20)), oriented_nodes=False
    )

    return count_cheats(maze, max_cheat_length_ps=2, min_time_savings_ps=100)


def solve_part_two():
    maze = Maze.from_map(
        '\n'.join(utilities.input_lines(year=2024, day=20)), oriented_nodes=False
    )

    return count_cheats(maze, max_cheat_length_ps=20, min_time_savings_ps=100)


def count_cheats(maze, max_cheat_length_ps, min_time_savings_ps, verbose_output=False):
    finish_line = list(maze.ends)[0]
    path, ps_cheatless = maze.find_cheapest_paths_astar()[finish_line]

    cheats = deque()
    indexed_path = list(enumerate(path))
    for index, point in tqdm(indexed_path):
        for later_index, later_point in indexed_path[index + 1:]:
            cheat_length_ps = taxicab(point, later_point)
            time_savings = later_index - index - cheat_length_ps
            if (
                    cheat_length_ps <= max_cheat_length_ps
                    and time_savings >= min_time_savings_ps
            ):
                # NOTE: We are NOT verifying that there is a contiguous wall
                #       between these points. This maze and the requirements
                #       for picosecond savings and cheat lengths appear to be
                #       constructed in such a way that
                #           path point --> cheat --> path point --> cheat --> path
                #       never yields a suitable cheat.
                cheats.append((point, later_point, time_savings))

    output = str(len(cheats))
    if verbose_output:
        output = '\n'.join([
            *(
                (
                    f'There are {len(list(cheat_group))} cheats that save '
                    f'{time_savings} picoseconds.'
                )
                for time_savings, cheat_group in itertools.groupby(
                    sorted(cheats, key=lambda cheat: cheat[2]),
                    key=lambda cheat: cheat[2]
                )
            ),
            (
                f'\nTotal cheats that save {min_time_savings_ps}+ '
                f'picoseconds: {output}'
            )
        ])
    return output


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())