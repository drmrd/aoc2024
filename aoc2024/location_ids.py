from collections import Counter


def similarity_score(list1, list2):
    list2_occurrences = Counter(list2)
    return sum(list1_id * list2_occurrences[list1_id] for list1_id in list1)


def compare_lists(list1, list2):
    return sum(
        abs(id1 - id2)
        for id1, id2 in paired_ids(list1, list2)
    )


def paired_ids(list1, list2):
    for pair in zip(sorted(list1), sorted(list2)):
        yield pair