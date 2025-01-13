import heapq
import itertools
from dataclasses import dataclass


@dataclass
class HeapEntry[T]:
    element: T
    priority: float
    count: int

    def __lt__(self, other):
        return (
            (self.priority, self.count, self.element)
            < (other.priority, other.count, other.element)
        )


class PriorityQueue[T]:
    def __init__(
            self,
            prioritized_elements: list[tuple[T, float]] | None = None
    ):
        if prioritized_elements is None:
            prioritized_elements = []

        self._heap = []
        self._heap_entry_finder: dict[T, HeapEntry[T]] = {}
        self._REMOVED = '<removed-task>'
        self._counter = itertools.count()

        for element, priority in prioritized_elements:
            self.add(element, priority)

    def __bool__(self):
        return bool(self._heap)

    def add(self, element: T, priority: float = 0):
        'Add a new task or update the priority of an existing task'
        if element in self._heap_entry_finder:
            self.remove(element)
        entry = HeapEntry(element, priority, next(self._counter))
        self._heap_entry_finder[element] = entry
        heapq.heappush(self._heap, entry)  # type: ignore

    def remove(self, element: HeapEntry[T]):
        'Mark an existing task as REMOVED. Raise KeyError if not found.'
        entry = self._heap_entry_finder.pop(element)
        entry.element = self._REMOVED

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self._heap:
            entry = heapq.heappop(self._heap)
            if (element := entry.element) is not self._REMOVED:
                del self._heap_entry_finder[element]
                return element, entry.priority
        raise KeyError('pop from an empty priority queue')
