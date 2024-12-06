from aoc2024 import printer, utilities


def solve_part_one():
    rules_and_lists = list(utilities.input_lines(day=5))
    dividing_line = rules_and_lists.index('')
    rules = rules_and_lists[:dividing_line]
    lists = [
        [int(page_number) for page_number in page_list.split(',')]
        for page_list in rules_and_lists[dividing_line + 1:]
    ]
    valid_page_lists = printer.valid_safety_manual_updates(rules, lists)
    return sum(
        page_list[len(page_list) // 2]
        for page_list in valid_page_lists
    )


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())