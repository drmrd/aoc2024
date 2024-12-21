from __future__ import annotations

import copy
import itertools
from collections import deque
from collections.abc import Hashable, Set, Sequence, Mapping
from functools import cached_property, cache
from typing import Any


class Graph[T: Hashable]:
    def __init__(
            self,
            *edges: *(tuple[T, T] | tuple[T, T, Any]),
            default_edge_weight: Any = None
    ):
        self._edges: list[tuple[T, T]] = [
            (source, target) for source, target, *_ in edges
        ]
        self._edge_weights: dict[tuple[T, T], dict[str, Any]] = {}
        for source, target, *weight in edges:
            if len(weight) > 1:
                raise ValueError(
                    'Providing multiple weights per edge in tuples passed to '
                    'the constructor is not supported.'
                )
            self._edge_weights[source, target] = {
                'weight': weight[0] if weight else default_edge_weight
            }
        self._nodes = list({
            *(source_node for source_node, _ in self._edges),
            *(target_node for _, target_node in self._edges)
        })

    @cached_property
    def edges(self) -> EdgeView[T]:
        return EdgeView(self._edges, self._edge_weights)

    @cached_property
    def nodes(self) -> list[T]:
        return self._nodes


class DiGraph[T: Hashable]:
    def __init__(self, *edges):
        self._edges = list(edges)
        self._nodes = list({
            *(source_node for source_node, _ in edges),
            *(target_node for _, target_node in edges)
        })
        self._adjacency_map = {
            (source, target): (source, target) in self._edges
            for source, target in itertools.product(self._nodes, repeat=2)
        }

    @cached_property
    def edges(self) -> list[tuple[T, T]]:
        return self._edges

    @cached_property
    def nodes(self) -> list[T]:
        return self._nodes

    @cache
    def parents(self, child: T) -> set[T]:
        return {
            parent
            for parent in self.nodes
            if self._adjacency_map[parent, child]
        }

    @cache
    def children(self, parent: T) -> set[T]:
        return {
            child
            for child in self.nodes
            if self._adjacency_map[parent, child]
        }

    def sort_topologically(self) -> list[T]:
        sorted_nodes: deque[T] = deque()
        orphans = {node for node in self.nodes if not self.parents(node)}
        remaining_nodes = set(self.nodes) - orphans
        remaining_edges = copy.copy(self.edges)

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


class EdgeView[T: Hashable](Mapping, Set):
    def __init__(
            self,
            edges: Sequence[tuple[T, T]],
            edge_weights: Mapping[tuple[T, T], Mapping[str, Any]]
    ):
        self._edges = edges
        self._edge_weights = edge_weights

    def __getitem__(self, key, /):
        return self._edge_weights[key]

    def __contains__(self, item):
        return (
            tuple(item) in self._edges
            or tuple(item)[::-1] in self._edges
        )

    def __iter__(self):
        return iter(self._edges)

    def __len__(self):
        return len(self._edges)