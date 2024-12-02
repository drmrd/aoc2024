from aoc2024 import location_ids, utilities


def solution_to_part_one():
    puzzle_inputs = [
        [int(location_id) for location_id in line.split()]
        for line in utilities.input_lines(day=1)
    ]
    list1 = [first_id for first_id, _ in puzzle_inputs]
    list2 = [second_id for _, second_id in puzzle_inputs]
    return location_ids.compare_lists(list1, list2)


def solution_to_part_two():
    puzzle_inputs = [
        [int(location_id) for location_id in line.split()]
        for line in utilities.input_lines(day=1)
    ]
    list1 = [first_id for first_id, _ in puzzle_inputs]
    list2 = [second_id for _, second_id in puzzle_inputs]
    return location_ids.similarity_score(list1, list2)


if __name__ == '__main__':
    print('Solution to Part 1:', solution_to_part_one())
    print('Solution to Part 2:', solution_to_part_two())