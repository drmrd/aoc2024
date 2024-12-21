from __future__ import annotations

import heapq
import math
from collections import deque, defaultdict
from collections.abc import Hashable, Set, Sequence, Mapping
from functools import cached_property, cache
from typing import Any, Union

type Node[T: Hashable] = T
type Edge[T: Hashable] = tuple[T, T]


class CycleError(ValueError):
    pass


class Graph[T: Hashable]:
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

    @cache
    def neighbors(self, node: Node) -> Set[T]:
        return self._neighbors[node]

    @cache
    def shortest_path(
            self,
            source: Node,
            target: Node | None = None,
            with_distance: bool = True
    ) -> Union[
            Sequence[Node],
            tuple[Sequence[Node], float],
            Mapping[Node, Sequence[Node]],
            Mapping[Node, tuple[Sequence[Node], float]]
    ]:
        distance_from_source: defaultdict[Node, float] = defaultdict(
            lambda: math.inf
        )
        distance_from_source[source] = 0
        previous = {source: None}
        heap = [(0, source)]

        while heap:
            distance_to_node, node = heapq.heappop(heap)

            for neighbor in self.neighbors(node):
                distance_to_neighbor = (
                    distance_to_node + self.edges[node, neighbor]['weight']
                )
                if distance_to_neighbor < distance_from_source[neighbor]:
                    distance_from_source[neighbor] = distance_to_neighbor
                    previous[neighbor] = node
                    heapq.heappush(heap, (distance_to_neighbor, neighbor))

        def prepare_path(
                target: Node,
                previous: Mapping[Node, Node],
                with_distance: bool
        ):
            if target in previous:
                path = _ancestor_sequence(target, previous)
            else:
                path = None

            if with_distance:
                return path, distance_from_source.get(target, math.inf)
            else:
                return path

        if target is not None:
            return prepare_path(target, previous, with_distance)
        else:
            return {
                target: prepare_path(target, previous, with_distance)
                for target in self.nodes
            }


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
) -> Sequence[Edge[T]]:
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
) -> Sequence[Node[T]]:
    return list({
        *(source_node for source_node, _ in edges),
        *(target_node for _, target_node in edges)
    })


def _ancestor_sequence[T: Hashable](
        node: Node[T],
        predecessor_tree: Mapping[Node[T], Node[T] | None],
        seen: set[Node[T]] | None = None,
        sequence: deque[Node[T]] | None = None
) -> Sequence[Node[T]]:
    if seen is None:
        seen = set()
    if sequence is None:
        sequence = deque([node])
    if (previous_node := predecessor_tree[node]) is not None:
        if previous_node in seen:
            raise CycleError('Cycle detected in predecessor tree.')

        sequence.appendleft(previous_node)
        seen.add(previous_node)
        return _ancestor_sequence(
            previous_node, predecessor_tree, seen, sequence
        )
    else:
        return list(sequence)