import pytest

from aoc2024.defrag import DiskMap


@pytest.fixture
def example_dense_disk_map():
    return '2333133121414131402'


def test_disk_map_parsing_day9_part1_example(example_dense_disk_map):
    disk_map = DiskMap.from_dense_map(example_dense_disk_map)
    map_string = ''.join(
        str(block_id) if block_id is not None else '.'
        for block_id in disk_map.block_ids
    )
    assert map_string == '00...111...2...333.44.5555.6666.777.888899'


def test_disk_map_backfill_day9_part1_example(example_dense_disk_map):
    backfilled_disk_map = DiskMap.from_dense_map(example_dense_disk_map).back_fill()
    backfilled_map_string = ''.join(
        str(block_id) if block_id is not None else '.'
        for block_id in backfilled_disk_map.block_ids
    )

    assert backfilled_map_string == '0099811188827773336446555566..............'


def test_disk_map_backfilled_checksum_day9_part1_example(example_dense_disk_map):
    backfilled_checksum = (
        DiskMap.from_dense_map(example_dense_disk_map)
               .back_fill()
               .checksum
    )

    assert backfilled_checksum == 1928


def test_disk_map_defrag_day9_part2_example(example_dense_disk_map):
    defragged_disk_map = DiskMap.from_dense_map(example_dense_disk_map).defrag()
    defragged_map_string = ''.join(
        str(block_id) if block_id is not None else '.'
        for block_id in defragged_disk_map.block_ids
    )

    assert defragged_map_string == '00992111777.44.333....5555.6666.....8888..'


def test_disk_map_defrag_day9_part2_example_extended(example_dense_disk_map):
    initial_block_ids = [
        0, 0, None, None, None, 1, 1, 1, None, None, None, 2, None, None, None,
        3, 3, 3, None, 4, 4, None, 5, 5, 5, 5, None, 6, 6, 6, 6, None, 7, 7, 7,
        None, 8, 8, 8, 8, 9, 9, None, None, None, None, 10, 10, 11, 11
    ]
    defragged_disk_map = DiskMap(initial_block_ids).defrag()

    expected_block_ids = [
        0, 0, 11, 11, 2, 1, 1, 1, 10, 10, None, None, 9, 9, None,
        3, 3, 3, None, 4, 4, None, 5, 5, 5, 5, None, 6, 6, 6, 6, None, 7, 7, 7,
        None, 8, 8, 8, 8, None, None, None, None, None, None, None, None, None,
        None
    ]
    assert defragged_disk_map.block_ids == expected_block_ids
    [0, 0, 11, 11, 2, 1, 1, 1, 10, 10, None, None, 9, 9, None, 3, 3, 3, None, 4, 4, None, 5, 5, 5, 5, None,
     6, 6, 6, 6, None, 7, 7, 7, None, None, None, None, None, None, None, 8, 8, 8, 8, None, None, None, None]
    [0, 0, 11, 11, 2, 1, 1, 1, 10, 10, None, None, 9, 9, None, 3, 3, 3, None, 4, 4, None, 5, 5, 5, 5, None,
     6, 6, 6, 6, None, 7, 7, 7, None, 8, 8, 8, 8, None, None, None, None, None, None, None, None, None, None]


def test_disk_map_defrag_checksum_day9_part2_example(example_dense_disk_map):
    defragged_checksum = (
        DiskMap.from_dense_map(example_dense_disk_map)
               .defrag()
               .checksum
    )

    assert defragged_checksum == 2858