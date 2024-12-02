from aoc2024 import location_ids, utilities


def solve_part_one():
    return location_ids.compare_lists(*_location_id_lists())


def solve_part_two():
    return location_ids.similarity_score(*_location_id_lists())


def _location_id_lists() -> tuple[list[int], list[int]]:
    puzzle_inputs = [
        [int(location_id) for location_id in line.split()]
        for line in utilities.input_lines(day=1)
    ]
    list1 = [first_id for first_id, _ in puzzle_inputs]
    list2 = [second_id for _, second_id in puzzle_inputs]
    return list1, list2


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())