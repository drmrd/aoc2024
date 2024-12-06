import itertools
from collections.abc import Iterator

from aoc2024.graph_theory import DiGraph


def correct_safety_manual_updates(
        page_ordering_rules: list[str], proposed_update_page_lists: list[list[int]]
) -> Iterator[list[int]]:
    rules_as_edges = [
        tuple(int(page) for page in rule.split('|'))
        for rule in page_ordering_rules
    ]
    for page_list in proposed_update_page_lists:
        page_set = set(page_list)
        page_list_rules = [
            rule_edge
            for rule_edge in rules_as_edges
            if set(rule_edge) <= page_set
        ]
        rules_graph: DiGraph[int] = DiGraph(*page_list_rules)
        totally_ordered_pages = rules_graph.sort_topologically()

        ordered_page_list_indices = [
            totally_ordered_pages.index(listed_page)
            for listed_page in page_list
            if listed_page in totally_ordered_pages
        ]
        if any(
                index_pair[0] >= index_pair[1]
                for index_pair in itertools.pairwise(ordered_page_list_indices)
        ):
            yield sorted(page_list, key=totally_ordered_pages.index)


def valid_safety_manual_updates(
        page_ordering_rules: list[str], proposed_update_page_lists: list[list[int]]
) -> Iterator[list[int]]:
    rules_as_edges = [
        tuple(int(page) for page in rule.split('|'))
        for rule in page_ordering_rules
    ]
    for page_list in proposed_update_page_lists:
        page_set = set(page_list)
        page_list_rules = [
            rule_edge
            for rule_edge in rules_as_edges
            if set(rule_edge) <= page_set
        ]
        rules_graph: DiGraph[int] = DiGraph(*page_list_rules)
        totally_ordered_pages = rules_graph.sort_topologically()

        ordered_page_list_indices = [
            totally_ordered_pages.index(listed_page)
            for listed_page in page_list
            if listed_page in totally_ordered_pages
        ]
        if all(
                index_pair[0] < index_pair[1]
                for index_pair in itertools.pairwise(ordered_page_list_indices)
        ):
            yield page_list