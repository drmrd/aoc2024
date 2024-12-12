from __future__ import annotations

from itertools import chain, repeat, zip_longest


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
