from __future__ import annotations

import heapq
import itertools
import math
from collections import deque, defaultdict
from collections.abc import Hashable, Set, Sequence, Mapping, Callable
from functools import cached_property, cache
from typing import Any, Union

type Node[T: Hashable] = T
type Edge[T: Hashable] = tuple[T, T]


class CycleError(ValueError):
    pass


class UndirectedGraph[T: Hashable]:
    def __init__(
            self,
            *edges: Edge[T] | tuple[*Edge[T], Any],
            default_edge_weight: Any = None
    ):
        self._edges = _build_edge_list(edges)
        self._edge_weights = _build_edge_weights_map(
            edges, default_edge_weight, self.is_directed
        )
        self._nodes = _build_node_list(self._edges)
        self._neighbors = {source: set() for source in self._nodes}
        for source, target in self._edges:
            self._neighbors[source].add(target)
            self._neighbors[target].add(source)

    @property
    def is_directed(self) -> bool:
        return False

    @cached_property
    def edges(self) -> EdgeView[Edge[T]]:
        return EdgeView(self._edges, self._edge_weights, self.is_directed)

    @cached_property
    def nodes(self) -> Sequence[Node[T]]:
        return self._nodes

    def add_node(self, node: Node[T]):
        if node in self._nodes:
            return
        self._nodes.append(node)
        self._neighbors[node] = set()

        try:
            del self.__dict__['nodes']
        except KeyError:
            pass

    def add_edge(self, edge: Edge[T]):
        self._edges.append(edge)
        for node in edge:
            self.add_node(node)

        self._neighbors[edge[0]].add(edge[1])
        self._neighbors[edge[1]].add(edge[0])

        self.neighbors.cache_clear()
        self.shortest_path.cache_clear()
        self.shortest_path_astar.cache_clear()

        try:
            del self.__dict__['edges']
        except KeyError:
            pass

    def remove_node(self, node: Node[T]):
        if node not in self._nodes:
            return
        self._nodes.remove(node)
        edges_to_remove = [edge for edge in self._edges if node in edge]
        for edge in edges_to_remove:
            self._edges.remove(edge)

        for neighbor in self._neighbors[node]:
            self._neighbors[neighbor].remove(node)
        del self._neighbors[node]
        self.neighbors.cache_clear()
        self.shortest_path.cache_clear()
        self.shortest_path_astar.cache_clear()

        for cached_property_name in ('nodes', 'edges'):
            try:
                del self.__dict__[cached_property_name]
            except KeyError:
                pass

    def remove_edge(self, edge: Edge[T]):
        to_remove = {edge}
        if not self.is_directed:
            to_remove.add(edge[::-1])
        for edge_to_remove in to_remove:
            try:
                self._edges.remove(edge_to_remove)
            except ValueError:
                continue

        self._neighbors[edge[0]].remove(edge[1])
        self._neighbors[edge[1]].remove(edge[0])

        self.neighbors.cache_clear()
        self.shortest_path.cache_clear()
        self.shortest_path_astar.cache_clear()

        try:
            del self.__dict__['edges']
        except KeyError:
            pass

    @cache
    def neighbors(self, node: Node) -> Set[T]:
        return self._neighbors[node]

    @cache
    def shortest_path(
            self,
            source: Node,
            target: Node | None = None,
            with_distance: bool = True,
            edge_weight = 'weight'
    ) -> Union[
            Sequence[Node],
            tuple[Sequence[Node], float],
            Mapping[Node, Sequence[Node]],
            Mapping[Node, tuple[Sequence[Node], float]]
    ]:
        if isinstance(edge_weight, str):
            def get_weight(edge):
                return self.edges[edge][edge_weight]
        else:
            def get_weight(edge):
                return edge_weight

        distance_from_source: defaultdict[Node, float] = defaultdict(
            lambda: math.inf
        )
        distance_from_source[source] = 0
        previous = {source: None}
        heap = [(0, source)]

        while heap:
            distance_to_node, node = heapq.heappop(heap)

            for neighbor in self.neighbors(node):
                current_distance = distance_from_source[neighbor]
                updated_distance = (
                    distance_to_node + get_weight((node, neighbor))
                )
                if updated_distance > current_distance:
                    continue
                elif updated_distance < current_distance:
                    distance_from_source[neighbor] = updated_distance
                    previous[neighbor] = {node}
                else:
                    previous[neighbor].add(node)
                heapq.heappush(
                    heap, (updated_distance, neighbor)
                )

        def prepare_paths(
                target: Node,
                previous: Mapping[Node, set[Node]],
                with_distance: bool
        ):
            if target in previous:
                paths = _ancestor_sequences(target, previous)
            else:
                paths = None

            if with_distance:
                return paths, distance_from_source.get(target, math.inf)
            else:
                return paths

        if target is not None:
            return prepare_paths(target, previous, with_distance)
        else:
            return {
                target: prepare_paths(target, previous, with_distance)
                for target in self.nodes
            }

    @cache
    def shortest_path_astar(
            self,
            source: Node,
            target: Node,
            heuristic: Callable[[Edge, Edge], float],
            edge_weight = 'weight'
    ) -> tuple[Sequence[Node], float]:
        if isinstance(edge_weight, str):
            def get_weight(edge):
                return self.edges[edge][edge_weight]
        else:
            def get_weight(edge):
                return edge_weight

        def recover_path(parent, end):
            current = end
            path = deque([current])
            while current in previous:
                current = previous[current]
                path.appendleft(current)
            return list(path)

        score_best_known: defaultdict[Node, float] = defaultdict(
            lambda: math.inf
        )
        # g_score
        score_best_known[source] = 0

        score_through_node: defaultdict[Node, float] = defaultdict(
            lambda: math.inf
        )
        # f_score
        score_through_node[source] = heuristic(source, target)

        open_set = []  # list of entries arranged in a heap
        entry_finder = {}  # mapping of tasks to entries
        REMOVED = '<removed-task>'  # placeholder for a removed task
        counter = itertools.count()  # unique sequence count

        def add_task(task, priority: float = 0):
            'Add a new task or update the priority of an existing task'
            if task in entry_finder:
                remove_task(task)
            count = next(counter)
            entry = [priority, count, task]
            entry_finder[task] = entry
            heapq.heappush(open_set, entry)

        def remove_task(task):
            'Mark an existing task as REMOVED. Raise KeyError if not found.'
            entry = entry_finder.pop(task)
            entry[-1] = REMOVED

        def pop_task():
            'Remove and return the lowest priority task. Raise KeyError if empty.'
            while open_set:
                priority, count, task = heapq.heappop(open_set)
                if task is not REMOVED:
                    del entry_finder[task]
                    return task, priority
            raise KeyError('pop from an empty priority queue')

        previous = {}
        add_task(source, score_through_node[source])

        while open_set:
            current, score_through = pop_task()

            if current == target:
                return recover_path(previous, target), score_through

            for neighbor in self._neighbors[current]:
                updated_best_known = (
                    score_best_known[current] + get_weight((current, neighbor))
                )
                if updated_best_known < score_best_known[neighbor]:
                    previous[neighbor] = current
                    score_best_known[neighbor] = updated_best_known
                    score_through_node[neighbor] = (
                        updated_best_known + heuristic(neighbor, target)
                    )
                    add_task(neighbor, score_through_node[neighbor])

        raise ValueError(f'Unable to find a path from {source} to {target}')


class DiGraph[T: Hashable]:
    def __init__(
            self,
            *edges: Edge | tuple[*Edge, Any],
            default_edge_weight: Any = None
    ):
        self._edges = _build_edge_list(edges)
        self._edge_weights = _build_edge_weights_map(
            edges, default_edge_weight, self.is_directed
        )
        self._nodes = _build_node_list(self._edges)

    @property
    def is_directed(self) -> bool:
        return True

    @cached_property
    def edges(self) -> EdgeView[Edge[T]]:
        return EdgeView(self._edges, self._edge_weights, self.is_directed)

    @cached_property
    def nodes(self) -> Sequence[T]:
        return self._nodes

    def add_node(self, node: Node[T]):
        if node in self._nodes:
            return
        self._nodes.append(node)

        try:
            del self.__dict__['nodes']
        except KeyError:
            pass

    def add_edge(self, edge: Edge[T]):
        self._edges.append(edge)
        for node in edge:
            self.add_node(node)

        self.parents.cache_clear()
        self.children.cache_clear()

        try:
            del self.__dict__['edges']
        except KeyError:
            pass

    def remove_node(self, node: Node[T]):
        if node not in self._nodes:
            return
        self._nodes.remove(node)
        edges_to_remove = [edge for edge in self._edges if node in edge]
        for edge in edges_to_remove:
            self._edges.remove(edge)

        self.parents.cache_clear()
        self.children.cache_clear()

        for cached_property_name in ('nodes', 'edges'):
            try:
                del self.__dict__[cached_property_name]
            except KeyError:
                pass

    def remove_edge(self, edge: Edge[T]):
        to_remove = {edge}
        if not self.is_directed:
            to_remove.add(edge[::-1])
        for edge_to_remove in to_remove:
            try:
                self._edges.remove(edge_to_remove)
            except ValueError:
                continue

        self.parents.cache_clear()
        self.children.cache_clear()

        try:
            del self.__dict__['edges']
        except KeyError:
            pass

    @cache
    def parents(self, child: T) -> set[T]:
        return {
            parent
            for parent in self.nodes
            if (parent, child) in self._edges
        }

    @cache
    def children(self, parent: T) -> set[T]:
        return {
            child
            for child in self.nodes
            if (parent, child) in self._edges
        }

    def sort_topologically(self) -> list[T]:
        sorted_nodes: deque[T] = deque()
        orphans = {node for node in self.nodes if not self.parents(node)}
        remaining_nodes = set(self.nodes) - orphans
        remaining_edges = set(self.edges)

        while orphans:
            orphan = orphans.pop()
            sorted_nodes.append(orphan)
            unvisited_children = {
                child
                for child in remaining_nodes
                if (orphan, child) in remaining_edges
            }
            for unvisited_child in unvisited_children:
                remaining_edges.remove((orphan, unvisited_child))
                incoming_edges = {
                    (source, target)
                    for (source, target) in remaining_edges
                    if target == unvisited_child
                }
                if not incoming_edges:
                    orphans.add(unvisited_child)
                    remaining_nodes.remove(unvisited_child)

        return list(sorted_nodes)


class EdgeView[Edge: Hashable](Mapping, Set):
    def __init__(
            self,
            edges: Sequence[Edge],
            edge_weights: Mapping[Edge, Mapping[str, Any]],
            directed: bool
    ):
        self._edges = edges
        self._edge_weights = edge_weights
        self._directed = directed

    def __getitem__(self, key, /):
        return self._edge_weights[tuple(key)]

    def __contains__(self, item):
        return (
            tuple(item) in self._edges
            or (
                not self._directed
                and tuple(item)[::-1] in self._edges
            )
        )

    def __iter__(self):
        return iter(self._edges)

    def __len__(self):
        return len(self._edges)


def _build_edge_list[T: Hashable](
        weighted_edges: tuple[Edge[T] | tuple[*Edge[T], Any], ...]
) -> list[Edge[T]]:
    return [
        (source, target) for source, target, *_ in weighted_edges
    ]


def _build_edge_weights_map[T: Hashable](
        weighted_edges: tuple[Edge[T] | tuple[*Edge[T], Any], ...],
        default_edge_weight: Any,
        directed: bool
) -> Mapping[Edge[T], dict[str, Any]]:
    edge_weights = {}
    for source, target, *weight in weighted_edges:
        if len(weight) > 1:
            raise ValueError(
                'Providing multiple weights per edge in tuples passed to '
                'the constructor is not supported.'
            )
        edge_weights[source, target] = {
            'weight': weight[0] if weight else default_edge_weight
        }
        if not directed:
            edge_weights[target, source] = edge_weights[source, target]
    return edge_weights


def _build_node_list[T: Hashable](
        edges: Sequence[Edge[T]]
) -> list[Node[T]]:
    return list({
        *(source_node for source_node, _ in edges),
        *(target_node for _, target_node in edges)
    })


def _ancestor_sequences[T: Hashable](
        node: Node[T],
        predecessor_set: Mapping[Node[T], set[Node[T]] | None],
        sequence_tails: list[list[Node[T]]] | None = None
) -> Sequence[Sequence[Node[T]]]:
    if sequence_tails is None:
        sequence_tails = [[node]]
    predecessors = predecessor_set[node]
    if predecessors is None:
        return sequence_tails
    ancestor_sequences = []
    for predecessor in predecessors:
        ancestor_sequences.extend(
            _ancestor_sequences(
                predecessor,
                predecessor_set,
                [[predecessor, *tail] for tail in sequence_tails]
            )
        )
    return ancestor_sequences


def grid2d(*shape):
    edges = set.union(*(
        {
            ((row, column), (row + 1, column)),
            ((row, column), (row, column + 1))
        }
        for row, column in itertools.product(*map(range, shape))
    ))
    return UndirectedGraph(*(
        (node, neighbor)
        for (node, neighbor) in edges
        if neighbor[0] < shape[0] and neighbor[1] < shape[1]
    ))