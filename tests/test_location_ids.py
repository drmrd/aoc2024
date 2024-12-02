from aoc2024.location_ids import compare_lists, similarity_score


def test_compare_lists_day01_example():
    assert compare_lists([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]) == 11


def test_similarity_score_day01_example():
    assert similarity_score([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]) == 31