from aoc2024 import utilities
from aoc2024.guard_simulator_2024 import GuardedLab


def solve_part_one():
    *_, lab = iter(GuardedLab(list(utilities.input_lines(day=6))))
    return lab.visited_count


def solve_part_two():
    lab = GuardedLab(list(utilities.input_lines(day=6)))
    guard_start_position = lab.guard_position
    guard_start_orientation = lab.guard_orientation

    *_, lab = iter(lab)
    visited_positions = lab.visited - {guard_start_position}
    number_of_loop_positions = 0
    for index, visited_position in enumerate(visited_positions):
        if index % 100 == 0:
            print('Testing position', index + 1, 'of', len(visited_positions))
        lab.reset()
        lab.add_guard(guard_start_position, guard_start_orientation)
        lab.block(visited_position)
        *_, lab = iter(lab)
        number_of_loop_positions += lab.guard_is_looping
        lab.unblock(visited_position)

    return number_of_loop_positions


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())