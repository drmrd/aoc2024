from aoc2024 import word_search


def test_count_finds_words_in_rows():
    puzzle = '\n'.join([
        'OOOXMASOOO',
        'XMASXMASOO',
        'OOOOOOXMAS'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 4
