import copy
from collections import deque


class DiGraph[T]:
    def __init__(self, *edges):
        self._edges = list(edges)
        self._nodes = list({
            *(source_node for source_node, _ in edges),
            *(target_node for _, target_node in edges)
        })

    @property
    def edges(self) -> list[tuple[T, T]]:
        return self._edges

    @property
    def nodes(self) -> list[T]:
        return self._nodes

    def parents(self, child: T) -> set[T]:
        return {parent for parent in self.nodes if (parent, child) in self.edges}

    def children(self, parent: T) -> set[T]:
        return {child for child in self.nodes if (parent, child) in self.edges}

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