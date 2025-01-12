from aoc2024 import utilities
from aoc2024.chronospatial_computer import ChronospatialComputer


def solve_part_one():
    computer = ChronospatialComputer()
    computer.load_debug_string('\n'.join(utilities.input_lines(year=2024, day=17)))
    program_output = computer.run_program()
    return ','.join(map(str, program_output))


def solve_part_two():
    computer = ChronospatialComputer()
    computer.load_debug_string('\n'.join(utilities.input_lines(year=2024, day=17)))
    return computer.find_minimal_register_a_state(
        desired_outputs=computer.program
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())