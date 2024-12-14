from __future__ import annotations

from itertools import chain, repeat, zip_longest, groupby
from operator import itemgetter


class DiskMap:
    def __init__(self, block_ids: list[int]):
        self.block_ids = block_ids

    @property
    def checksum(self) -> int:
        return sum(
            index * block_id
            for index, block_id in enumerate(self.block_ids)
            if block_id is not None
        )

    def back_fill(self) -> DiskMap:
        backfilled = DiskMap(self.block_ids[:])
        forward_index = 0
        reverse_index = len(backfilled.block_ids) - 1
        while 0 <= forward_index < reverse_index < len(backfilled.block_ids):
            if backfilled.block_ids[forward_index] is not None:
                forward_index += 1
                continue
            file_id = backfilled.block_ids[reverse_index]
            if file_id is None:
                reverse_index -= 1
                continue
            backfilled.block_ids[forward_index] = file_id
            backfilled.block_ids[reverse_index] = None
        return backfilled

    def defrag(self) -> DiskMap:
        defragged = DiskMap(self.block_ids[:])
        fragged_blocks = list(
            map(
                lambda key_group: (key_group[0], list(map(itemgetter(0), key_group[1]))),
                groupby(enumerate(defragged.block_ids[:]), key=itemgetter(1))
            )
        )
        free_segments = [
            {
                'index': block_indices[0],
                'length': len(block_indices)
            }
            for file_id, block_indices in fragged_blocks
            if file_id is None
        ]
        file_segments_tail = [
            {
                'file_id': file_id,
                'index': block_indices[0],
                'length': len(block_indices)
            }
            for file_id, block_indices in fragged_blocks
            if file_id is not None and file_id != 0
        ]
        for file_segment in reversed(file_segments_tail):
            for free_segment_index, free_segment in enumerate(free_segments):
                extra_free_space = (
                    free_segment['length'] - file_segment['length']
                )
                if extra_free_space >= 0 and file_segment['index'] > free_segment['index']:
                    for offset in range(file_segment['length']):
                        defragged.block_ids[free_segment['index'] + offset] = (
                            file_segment['file_id']
                        )
                        defragged.block_ids[file_segment['index'] + offset] = (
                            None
                        )
                    free_segment['index'] += file_segment['length']
                    free_segment['length'] = extra_free_space
                    break
            if free_segment['length'] == 0:
                del free_segments[free_segment_index]
        return defragged

    @staticmethod
    def from_dense_map(dense_map: str) -> DiskMap:
        block_ids = chain.from_iterable(
            chain.from_iterable((
            (repeat(file_id, int(file_blocks)), repeat(None, int(free_blocks)))
            for file_id, (file_blocks, free_blocks) in enumerate(
                zip_longest(dense_map[::2], dense_map[1::2], fillvalue=0)
            )
        )))
        return DiskMap(list(block_ids))
