from aoc2024.printer import (
    correct_safety_manual_updates,
    valid_safety_manual_updates
)


def test_valid_safety_manual_updates_day05_part1_example():
    actual_valid_update_page_lists = valid_safety_manual_updates(
        page_ordering_rules=[
            '47|53', '97|13', '97|61', '97|47', '75|29', '61|13', '75|53',
            '29|13', '97|29', '53|29', '61|53', '97|53', '61|29', '47|13',
            '75|47', '97|75', '47|61', '75|61', '47|29', '75|13', '53|13'
        ],
        proposed_update_page_lists=[
            [75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13],
            [75, 97, 47, 61, 53], [61, 13, 29], [97, 13, 75, 29, 47]
        ]
    )

    expected_valid_update_page_lists = [
        [75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13]
    ]
    assert list(actual_valid_update_page_lists) == expected_valid_update_page_lists


def test_correct_safety_manual_updates_day05_part2_example():
    actual_corrected_page_lists = correct_safety_manual_updates(
        page_ordering_rules=[
            '47|53', '97|13', '97|61', '97|47', '75|29', '61|13', '75|53',
            '29|13', '97|29', '53|29', '61|53', '97|53', '61|29', '47|13',
            '75|47', '97|75', '47|61', '75|61', '47|29', '75|13', '53|13'
        ],
        proposed_update_page_lists=[
            [75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13],
            [75, 97, 47, 61, 53], [61, 13, 29], [97, 13, 75, 29, 47]
        ]
    )

    expected_corrected_page_lists = [
        [97, 75, 47, 61, 53], [61, 29, 13], [97, 75, 47, 29, 13]
    ]
    assert list(actual_corrected_page_lists) == expected_corrected_page_lists