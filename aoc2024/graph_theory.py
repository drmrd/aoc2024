from __future__ import annotations

import heapq
import itertools
import math
from collections import deque, defaultdict
from collections.abc import Hashable, Set, Sequence, Mapping, Callable
from copy import deepcopy
from functools import cached_property, cache, lru_cache
from typing import Any, Union, Generator

from aoc2024.collections import PriorityQueue

type Node[T: Hashable] = T
type Edge[T: Hashable] = tuple[T, T]


class UndirectedGraph[T: Hashable]:
    def __init__(
            self,
            *edges: Edge[T] | tuple[*Edge[T], Any],
            default_edge_weight: Any = None
    ):
        self._nodes, self._edges = _build_attributes_maps(
            edges, default_edge_weight, self.is_directed
        )
        self._neighbors: dict[Node[T], set[Node[T]]] = {
            node: set(self._edges.get(node, set())) for node in self._nodes
        }
        for target in self._nodes:
            for source in self._edges:
                if target in self._edges[source]:
                    self._neighbors[target].add(source)
        self._in_nodes = self._out_nodes = self._neighbors

    def __getitem__(self, edge: Edge[T]):
        return self._edges[edge[0]][edge[1]]

    @property
    def is_directed(self) -> bool:
        return False

    @cached_property
    def edges(self) -> EdgeView[Edge[T]]:
        return EdgeView(self._edges, self.is_directed)

    @cached_property
    def nodes(self) -> Sequence[Node[T]]:
        return self._nodes

    def add_node(self, node: Node[T]):
        if node in self._nodes:
            return
        self._nodes[node] = {}
        self._neighbors[node] = set()

        try:
            del self.__dict__['nodes']
        except KeyError:
            pass

    def add_edge(self, edge: Edge[T]):
        source, target = edge
        self._edges.setdefault(source, {}).setdefault(target, {})
        for node in edge:
            self.add_node(node)

        self._neighbors[source].add(target)
        self._neighbors[target].add(source)

        self._clear_caches()

    def remove_node(self, node: Node[T]):
        if node not in self._nodes:
            return
        del self._nodes[node]
        for neighbor in self._neighbors[node]:
            self._neighbors[neighbor].remove(node)
            try:
                del self._edges[neighbor][node]
            except KeyError:
                continue
        del self._neighbors[node]
        try:
            del self._edges[node]
        except KeyError:
            pass
        self._clear_caches()

    def remove_edge(self, edge: Edge[T]):
        to_remove = {edge}
        if not self.is_directed:
            to_remove.add(edge[::-1])
        for source, target in to_remove:
            try:
                del self._edges[source][target]
            except KeyError:
                continue

        self._neighbors[edge[0]].remove(edge[1])
        self._neighbors[edge[1]].remove(edge[0])
        self._clear_caches()

    def to_directed(self) -> DiGraph[T]:
        return DiGraph(
            *itertools.chain.from_iterable(
                (
                    (source, target, self[source, target]),
                    (target, source, self[source, target])
                )
                for source, target in self.edges
            )
        )

    @cache
    def neighbors(self, node: Node[T]) -> Set[T]:
        return self._neighbors[node]

    @cache
    def in_edges(self, node: Node[T]) -> set[Edge[T]]:
        return {(neighbor, node) for neighbor in self._in_nodes[node]}

    @cache
    def out_edges(self, node: Node[T]) -> set[Edge[T]]:
        return {(node, neighbor) for neighbor in self._out_nodes[node]}

    def in_nodes(self, node: Node[T]) -> set[Node[T]]:
        return self.neighbors(node)

    def out_nodes(self, node: Node[T]) -> set[Node[T]]:
        return self.neighbors(node)

    @cache
    def cliques(self) -> Sequence[set[Node[T]]]:
        return list(_ibk_gpx(self, set(), set(self.nodes), set()))

    @cache
    def all_shortest_paths(
            self,
            source: Node[T],
            target: Node[T] | None = None,
            with_distance: bool = True,
            edge_weight = 'weight'
    ) -> Union[
            Sequence[Node[T]],
            tuple[Sequence[Node[T]], float],
            Mapping[Node[T], Sequence[Node[T]]],
            Mapping[Node[T], tuple[Sequence[Node[T]], float]]
    ]:
        if target is None:
            return all_shortest_paths(
                graph=self,
                source=source,
                with_distance=with_distance,
                edge_weight=edge_weight
            )
        else:
            return all_shortest_paths_to_targets(
                graph=self,
                source=source,
                targets=[target] if target in self.nodes else target,
                with_distance=with_distance,
                edge_weight=edge_weight
            )

    @cache
    def shortest_path(
            self,
            source: Node[T],
            target: Node[T],
            heuristic: Callable[[Node[T], Node[T]], float],
            edge_weight = 'weight'
    ) -> tuple[Sequence[Node[T]], float]:
        return shortest_path(self, source, target, heuristic, edge_weight)

    def _clear_caches(self):
        self.in_edges.cache_clear()
        self.out_edges.cache_clear()
        self.neighbors.cache_clear()
        self.cliques.cache_clear()
        self.all_shortest_paths.cache_clear()
        self.shortest_path.cache_clear()

        for cached_property_name in ('nodes', 'edges'):
            try:
                del self.__dict__[cached_property_name]
            except KeyError:
                pass


class DiGraph[T: Hashable]:
    def __init__(
            self,
            *edges: Edge[T] | tuple[*Edge[T], Any],
            default_edge_weight: Any = None
    ):
        self._nodes, self._edges = _build_attributes_maps(
            edges, default_edge_weight, self.is_directed
        )
        self._in_nodes = {node: set() for node in self.nodes}
        self._out_nodes: dict[Node[T], set[Node[T]]] = {
            node: set(self._edges.get(node, set())) for node in self.nodes
        }
        for source in self._edges:
            for target in self._edges[source]:
                self._in_nodes[target].add(source)

    def __getitem__(self, edge: Edge[T]):
        return self._edges[edge[0]][edge[1]]

    @property
    def is_directed(self) -> bool:
        return True

    @cached_property
    def edges(self) -> EdgeView[Edge[T]]:
        return EdgeView(self._edges, self.is_directed)

    @cache
    def in_edges(self, node: Node[T]) -> set[Edge[T]]:
        return {(neighbor, node) for neighbor in self._in_nodes[node]}

    @cache
    def out_edges(self, node: Node[T]) -> set[Edge[T]]:
        return {(node, neighbor) for neighbor in self._out_nodes[node]}

    @cached_property
    def nodes(self) -> Sequence[T]:
        return self._nodes

    def add_node(self, node: Node[T]):
        if node in self._nodes:
            return
        self._nodes[node] = {}
        self._in_nodes[node] = set()
        self._out_nodes[node] = set()

        try:
            del self.__dict__['nodes']
        except KeyError:
            pass

    def add_edge(self, edge: Edge[T]):
        source, target = edge
        self._edges.setdefault(source, {}).setdefault(target, {})
        for node in edge:
            self.add_node(node)

        if source not in self._out_nodes:
            self._out_nodes[source] = set()
        if target not in self._in_nodes:
            self._in_nodes[target] = set()
        self._out_nodes[source].add(target)
        self._in_nodes[target].add(source)

        self._clear_caches()

    def remove_node(self, node: Node[T]):
        if node not in self._nodes:
            return
        del self._nodes[node]

        for out_node in self._out_nodes[node]:
            self._in_nodes[out_node].remove(node)
            try:
                del self._edges[out_node][node]
            except KeyError:
                continue
        del self._out_nodes[node]

        for in_node in self._in_nodes[node]:
            self._out_nodes[in_node].remove(node)
            try:
                del self._edges[in_node][node]
            except KeyError:
                continue
        del self._in_nodes[node]

        try:
            del self._edges[node]
        except KeyError:
            pass
        self._clear_caches()

    def remove_edge(self, edge: Edge[T]):
        source, target = edge
        if source not in self._edges or target not in self._edges[source]:
            return

        del self._edges[source][target]
        self._out_nodes[source].remove(target)
        self._in_nodes[target].remove(source)
        self._clear_caches()

    @cache
    def in_nodes(self, node: Node[T]) -> set[Node[T]]:
        return self._in_nodes[node]

    @cache
    def out_nodes(self, node: Node[T]) -> set[Node[T]]:
        return self._out_nodes[node]

    def parents(self, child: Node[T]) -> set[Node[T]]:
        return self.in_nodes(child)

    def children(self, parent: Node[T]) -> set[Node[T]]:
        return self.out_nodes(parent)

    @cache
    def all_shortest_paths(
            self,
            source: Node[T],
            target: Node[T] | Sequence[Node[T]] | None = None,
            with_distance: bool = True,
            edge_weight = 'weight'
    ) -> Union[
            Sequence[Node[T]],
            tuple[Sequence[Node[T]], float],
            Mapping[Node[T], Sequence[Node[T]]],
            Mapping[Node[T], tuple[Sequence[Node[T]], float]]
    ]:
        if target is None:
            return all_shortest_paths(
                graph=self,
                source=source,
                with_distance=with_distance,
                edge_weight=edge_weight
            )
        else:
            return all_shortest_paths_to_targets(
                graph=self,
                source=source,
                targets=[target] if target in self.nodes else target,
                with_distance=with_distance,
                edge_weight=edge_weight
            )

    @cache
    def shortest_path(
            self,
            source: Node[T],
            target: Node[T],
            heuristic: Callable[[Node[T], Node[T]], float],
            edge_weight = 'weight'
    ) -> tuple[Sequence[Node[T]], float]:
        return shortest_path(self, source, target, heuristic, edge_weight)

    @lru_cache(1)
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

    def _clear_caches(self):
        self.in_nodes.cache_clear()
        self.out_nodes.cache_clear()
        self.in_edges.cache_clear()
        self.out_edges.cache_clear()
        self.all_shortest_paths.cache_clear()
        self.shortest_path.cache_clear()
        self.sort_topologically.cache_clear()

        for cached_property_name in ('nodes', 'edges'):
            try:
                del self.__dict__[cached_property_name]
            except KeyError:
                pass


class EdgeView[T: Hashable](Mapping, Set):
    def __init__(
            self,
            edges: dict[Node[T], dict[Node[T], dict[str, Any]]],
            directed: bool
    ):
        self._edges = edges
        self._directed = directed

    def __getitem__(self, key, /):
        try:
            source, target = key
            return self._edges[source][target]
        except KeyError as key_error:
            if not self._directed:
                try:
                    return self._edges[target][source]
                except KeyError:
                    pass
            raise key_error
        except ValueError:
            return self._edges[key]

    def __contains__(self, item):
        try:
            source, target = item
        except ValueError:
            return False
        return (
            source in self._edges and target in self._edges[source]
            or (
                not self._directed
                and target in self._edges and source in self._edges[target]
            )
        )

    def __iter__(self):
        seen = set()
        if not self._directed:
            def update_seen(source, target):
                nonlocal seen
                seen |= {(source, target), (target, source)}
        else:
            def update_seen(*_):
                pass

        for source in self._edges:
            for target in self._edges[source]:
                if (source, target) not in seen:
                    yield source, target
                update_seen(source, target)

    @lru_cache(1)
    def __len__(self):
        return len(list(self))


def _build_edge_list[T: Hashable](
        weighted_edges: tuple[Edge[T] | tuple[*Edge[T], Any], ...]
) -> list[Edge[T]]:
    return [
        (source, target) for source, target, *_ in weighted_edges
    ]


def _build_attributes_maps[T: Hashable](
        weighted_edges: tuple[Edge[T] | tuple[*Edge[T], Any], ...],
        default_edge_weight: Any,
        directed: bool
) -> tuple[
        dict[Node[T], dict[str, Any]],
        dict[Node[T], dict[Node[T], dict[str, Any]]]
]:
    node_attributes = {}
    edge_attributes = {}
    for source, target, *rest in weighted_edges:
        node_attributes.setdefault(source, {})
        node_attributes.setdefault(target, {})
        if len(rest) > 1:
            raise ValueError(
                'Providing multiple weights or attribute dictionaries per '
                'edge in tuples passed to the constructor is not supported.'
            )
        if source in edge_attributes and target in edge_attributes[source]:
            raise ValueError(
                'Attempting to construct a graph with multiple copies of edge '
                f'{(source, target)}.'
            )
        else:
            edge_attributes.setdefault(source, {})
        try:
            edge_attributes[source][target] = {
                key: value for key, value in rest[0].items()
            }
        except (IndexError, AttributeError):
            edge_attributes[source][target] = {
                'weight': rest[0] if rest else default_edge_weight
            }
    return node_attributes, edge_attributes


def _build_node_attributes_map[T: Hashable](
        edges: Sequence[Edge[T]]
) -> dict[Node[T], Any]:
    return {
        node: {}
        for node in {
            *(source_node for source_node, _ in edges),
            *(target_node for _, target_node in edges)
        }
    }


def _ibk_gpx[T: Hashable](
        graph: UndirectedGraph[T],
        clique: set,
        prospective_nodes: set,
        exclusions: set
) -> Generator[set[T]]:
    potential_pivots = prospective_nodes | exclusions
    if not potential_pivots:
        yield clique
        return
    pivot_node = potential_pivots.pop()
    pivot_neighbors = prospective_nodes & graph.neighbors(pivot_node)
    for node in potential_pivots:
        prospective_neighbors = prospective_nodes & graph.neighbors(node)
        if len(prospective_neighbors) > len(pivot_neighbors):
            pivot_neighbors = prospective_neighbors

    for node in prospective_nodes - pivot_neighbors:
        prospective_nodes.remove(node)
        yield from _ibk_gpx(
            graph,
            clique | {node},
            prospective_nodes & graph.neighbors(node),
            exclusions & graph.neighbors(node)
        )
        exclusions.add(node)


def all_shortest_paths[T: Hashable](
        graph: UndirectedGraph[T] | DiGraph[T],
        source: Node[T],
        with_distance: bool = True,
        edge_weight = 'weight'
) -> Union[
        Sequence[Node[T]],
        tuple[Sequence[Node[T]], float],
        Mapping[Node[T], Sequence[Node[T]]],
        Mapping[Node[T], tuple[Sequence[Node[T]], float]]
]:
    if not graph.is_directed:
        graph = graph.to_directed()  # type: ignore

    if isinstance(edge_weight, str):
        def get_weight(edge):
            return graph.edges[edge][edge_weight]
    else:
        def get_weight(edge):
            return edge_weight

    distance_from_source: defaultdict[Node[T], float] = defaultdict(
        lambda: math.inf
    )
    distance_from_source[source] = 0
    previous: dict[Node[T], set[Node[T]] | None] = {source: None}
    heap = [(0, source)]

    while heap:
        distance_to_node, node = heapq.heappop(heap)

        for out_edge in graph.out_edges(node):
            _, neighbor = out_edge
            current_distance = distance_from_source[neighbor]
            updated_distance = (
                distance_to_node + get_weight((node, neighbor))
            )
            if updated_distance > current_distance:
                continue
            elif updated_distance < current_distance:
                distance_from_source[neighbor] = updated_distance
                previous[neighbor] = {node}  # type: ignore
            else:
                previous[neighbor].add(node)  # type: ignore
            heapq.heappush(
                heap, (updated_distance, neighbor)
            )

    def prepare_paths(
            target: Node[T],
            previous: Mapping[Node[T], set[Node[T]] | None],
            with_distance: bool
    ):
        if target in previous:
            paths = _recover_all_paths(target, previous)
        else:
            paths = []

        if with_distance:
            return paths, distance_from_source.get(target, math.inf)
        else:
            return paths

    return {
        target: prepare_paths(target, previous, with_distance)
        for target in graph.nodes
    }


def all_shortest_paths_to_targets[T: Hashable](
        graph: UndirectedGraph[T] | DiGraph[T],
        source: Node[T],
        targets: list[Node[T]],
        with_distance: bool = True,
        edge_weight = 'weight'
) -> Union[
        Sequence[Node[T]],
        tuple[Sequence[Node[T]], float],
        Mapping[Node[T], Sequence[Node[T]]],
        Mapping[Node[T], tuple[Sequence[Node[T]], float]]
]:
    if not targets:
        raise ValueError('At least one target node must be provided.')
    if not graph.is_directed:
        graph = graph.to_directed()  # type: ignore

    if isinstance(edge_weight, str):
        def get_weight(edge):
            return graph.edges[edge][edge_weight]
    else:
        def get_weight(edge):
            return edge_weight

    distance_from_source: defaultdict[Node[T], float] = defaultdict(
        lambda: math.inf
    )
    distance_from_source[source] = 0
    heap = [(0, source, {source})]

    best_paths = {target: deque() for target in targets}
    shortest_distance = {target: None for target in targets}
    while heap:
        distance_to_node, node, path = heapq.heappop(heap)

        if node in targets:
            cheapest_path_cost = shortest_distance[node]
            if cheapest_path_cost is None or distance_to_node == cheapest_path_cost:
                best_paths[node].append(path)
                shortest_distance[node] = distance_to_node
            continue

        for out_edge in graph.out_edges(node):
            _, neighbor = out_edge
            current_distance = distance_from_source[neighbor]
            updated_distance = (
                distance_to_node + get_weight((node, neighbor))
            )
            if updated_distance > current_distance:
                continue
            elif updated_distance < current_distance:
                distance_from_source[neighbor] = updated_distance
            heapq.heappush(
                heap, (updated_distance, neighbor, path | {neighbor})
            )

    def target_output(
            target_paths: deque[Sequence[Node[T]]],
            target_distance: float | None
    ):
        paths = [list(path) for path in target_paths]
        if with_distance:
            distance = math.inf if target_distance is None else target_distance
            return paths, distance
        else:
            return paths
    if len(targets) == 1:
        return target_output(
            best_paths[targets[0]], shortest_distance[targets[0]]
        )
    else:
        return {
            target: target_output(
                best_paths[target], shortest_distance[target]
            ) for target in targets
        }


def shortest_path[T: Hashable](
        graph: UndirectedGraph[T] | DiGraph[T],
        source: Node[T],
        target: Node[T],
        heuristic: Callable[[Node[T], Node[T]], float],
        edge_weight='weight'
) -> tuple[Sequence[Node[T]], float]:
    if isinstance(edge_weight, str):
        def get_weight(edge):
            return graph.edges[edge][edge_weight]
    else:
        def get_weight(_):
            return edge_weight

    def recover_path(previous, end):
        current = end
        path = deque([current])
        while current in previous:
            current = previous[current]
            path.appendleft(current)
        return list(path)

    score_best_known: defaultdict[Node[T], float] = defaultdict(
        lambda: math.inf
    )
    # g_score
    score_best_known[source] = 0

    score_through_node: defaultdict[Node[T], float] = defaultdict(
        lambda: math.inf
    )
    # f_score
    score_through_node[source] = heuristic(source, target)

    queue = PriorityQueue()

    previous: dict[Node[T], Node[T]] = {}
    queue.add(source, score_through_node[source])

    while queue:
        current, score_through = queue.pop()

        if current == target:
            return recover_path(previous, target), score_through

        out_neighbors = {
            neighbor for _, neighbor in graph.out_edges(current)
            if neighbor != current
        }
        for neighbor in out_neighbors:
            updated_best_known = (
                    score_best_known[current] + get_weight((current, neighbor))
            )
            if updated_best_known < score_best_known[neighbor]:
                previous[neighbor] = current
                score_best_known[neighbor] = updated_best_known
                score_through_node[neighbor] = (
                        updated_best_known
                        + heuristic(neighbor, target)
                )
                queue.add(neighbor, score_through_node[neighbor])

    raise ValueError(f'Unable to find a path from {source} to {target}')


def _recover_all_paths[T: Hashable](
        node: Node[T],
        predecessor_set: Mapping[Node[T], set[Node[T]] | None],
        path_tails: Sequence[Sequence[Node[T]]] | None = None
) -> list[list[Node[T]]]:
    if path_tails is None:
        path_tails = deque([deque([node])])

    return [
        list(path)
        for path in _recover_all_paths_recurrence(
            node, predecessor_set, deque(deque(tail) for tail in path_tails)
        )
    ]


def _recover_all_paths_recurrence[T: Hashable](
        node: Node[T],
        predecessor_set: Mapping[Node[T], set[Node[T]] | None],
        path_tails: deque[deque[Node[T]]]
) -> deque[deque[Node[T]]]:
    predecessors = predecessor_set[node]
    if predecessors is None:
        return path_tails

    recovered_paths: deque[deque[Node[T]]] = deque()
    for predecessor in predecessors:
        predecessor_path_tails = deepcopy(path_tails)
        for tail in predecessor_path_tails:
            tail.appendleft(predecessor)
        recovered_paths.extend(
            _recover_all_paths_recurrence(
                predecessor,
                predecessor_set,
                predecessor_path_tails
            )
        )
    return recovered_paths


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