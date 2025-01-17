from aoc2024 import word_search


def test_cross_count_day04_example():
    puzzle = '\n'.join([
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX'
    ])
    assert word_search.cross_count(puzzle) == 9


def test_count_day04_example():
    puzzle = '\n'.join([
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 18


def test_count_finds_words_in_rows():
    puzzle = '\n'.join([
        'OOOXMASOOO',
        'XMASXMASOO',
        'OOOOOOXMAS'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 4


def test_count_finds_reversed_horizontal_words():
    puzzle = '\n'.join([
        'OOOSAMXOOO',
        'SAMXSAMXOO',
        'OOOOOOSAMX'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 4


def test_count_finds_words_in_columns():
    puzzle = '\n'.join([
        'OXOO',
        'OMOO',
        'OAOO',
        'XSOO',
        'MXOO',
        'AMOO',
        'SAXX',
        'OSMM',
        'OOAA',
        'OOSS'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 5


def test_count_finds_reversed_words_in_columns():
    puzzle = '\n'.join([
        'OOXO',
        'OOMO',
        'OOAO',
        'OOSX',
        'OOXM',
        'OOMA',
        'XXAS',
        'MMSO',
        'AAOO',
        'SSOO'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 5


def test_count_finds_words_on_diagonals():
    puzzle = '\n'.join([
        'OOXOXOOOOO',
        'OOOMSMSOOO',
        'OOAOAAAAOO',
        'OSOOMSMSMO',
        'OOOXOOOXOX'
    ])
    assert word_search.count(puzzle, words=['XMAS']) == 6