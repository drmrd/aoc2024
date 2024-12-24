import math

import pytest

from aoc2024.graph_theory import DiGraph, Graph


@pytest.mark.parametrize(
    'graph_class',
    (Graph, DiGraph)
)
class TestCommonProperties:
    def test_graph_can_be_constructed_from_edges(self, graph_class):
        expected_nodes = [0, 1, 2, 3, 4, 5, 6, 7]
        expected_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7),
            (7, 4)
        ]

        G = graph_class(*expected_edges)

        assert set(expected_nodes) == set(G.nodes)
        assert set(expected_edges) == set(G.edges)

    @pytest.mark.parametrize(
        'expected_default_weight',
        (None, '🚀🚀🚀', [1, 2.3, 4.56]),
        ids=('No default', 'Unicode string', 'List of numbers')
    )
    def test_graph_can_be_constructed_from_weighted_edges(
            self, graph_class, expected_default_weight
    ):
        expected_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 37, 53, 137]
        expected_weighted_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7),
            (7, 4)
        ]
        expected_unweighted_edges = [(0, 53), (1, 37), (2, 137)]
        expected_edge_weights = [sum(edge) for edge in expected_weighted_edges]

        G = graph_class(
            *(
                (source, target, weight)
                for (source, target), weight in zip(
                expected_weighted_edges, expected_edge_weights
            )
            ),
            *expected_unweighted_edges,
            default_edge_weight=expected_default_weight
        )

        assert set(expected_nodes) == set(G.nodes)
        assert {
            *expected_weighted_edges, *expected_unweighted_edges
        } == set(G.edges)

        for edge, expected_weight in zip(
                expected_weighted_edges, expected_edge_weights
        ):
            assert G.edges[edge]['weight'] == expected_weight

        for edge in expected_unweighted_edges:
            edge_weight = G.edges[edge]['weight']
            if expected_default_weight is None:
                assert edge_weight is expected_default_weight
            else:
                assert edge_weight == expected_default_weight

    def test_graph_edge_directedness(self, graph_class):
        expected_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7),
            (7, 4)
        ]

        G = graph_class(*expected_edges)

        for source, target in expected_edges:
            assert (source, target) in G.edges, (
                f'{(source, target)} not found in G.edges'
            )
            assert G.is_directed or (target, source) in G.edges, (
                f'Although G is undirected and {(source, target)} is in '
                f'G.edges, the reversed edge {(target, source)} is not.'
            )

    def test_can_add_nodes_to_graph(self, graph_class):
        expected_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)
        ]
        G = graph_class(*expected_edges)
        assert set(G.nodes) == set(range(8))

        G.add_node(8)
        G.add_node(9)

        assert set(G.nodes) == set(range(10))


class TestGraph:
    def test_can_retrieve_neighbors_of_a_given_node(self):
        G = Graph((0, 1), (1, 2), (2, 3), (3, 4), (3, 0), (0, 2), (0, 4))
        expected_neighbors_map = {
            0: {1, 2, 3, 4}, 1: {0, 2}, 2: {0, 1, 3}, 3: {0, 2, 4}, 4: {0, 3}
        }
        for node, expected_neighbors in expected_neighbors_map.items():
            actual_neighbors = G.neighbors(node)
            assert actual_neighbors == expected_neighbors, (
                f'Expected node {node} to have neighbors '
                f'{expected_neighbors}, but its actual neighbors are '
                f'{actual_neighbors}.'
            )

    def test_can_compute_all_shortest_paths_from_a_source_node(self):
        G = Graph(
            (0, 1, 5), (1, 2, 3), (2, 3, 7), (3, 4, 5),
            (0, 2, 7), (0, 4, 10),
            (10, 11, 1)
        )

        expected_distance = {
            0: 0, 1: 5, 2: 7, 3: 14, 4: 10, 10: math.inf, 11: math.inf
        }
        assert G.shortest_distance(0) == expected_distance

        for target in G.nodes:
            assert G.shortest_distance(0, target) == expected_distance[target]


class TestDiGraph:
    def test_can_retrieve_parents_and_children_of_a_given_node(self):
        G = DiGraph((0, 1), (1, 2), (2, 3), (3, 4), (3, 0), (0, 2), (0, 4))
        expected_parents = {0: {3}, 1: {0}, 2: {0, 1}, 3: {2}, 4: {0, 3}}
        expected_children = {0: {1, 2, 4}, 1: {2}, 2: {3}, 3: {0, 4}, 4: set()}

        for node, expected_parents in expected_parents.items():
            assert set(G.parents(node)) == expected_parents, (
                f'Node {node} has parents {G.parents(node)}, not the expected '
                f'parents {expected_parents}'
            )
        for node, expected_children in expected_children.items():
            assert set(G.children(node)) == expected_children, (
                f'Node {node} has children {G.children(node)}, not the '
                f'expected children {expected_children}'
            )

    def test_dags_can_be_topologically_sorted(self):
        DAG = DiGraph(
            # Weak Component 1:
            (0, 1), (1, 2), (2, 3), (3, 4), (0, 2), (0, 4),
            (5, 2), (5, 3), (5, 6), (5, 7), (5, 8),
            (9, 2), (9, 3), (9, 6), (9, 7), (9, 10), (9, 11),
            (7, 4), (7, 11), (8, 4), (8, 11),
            # Weak Component 2:
            (12, 13), (13, 14), (14, 15), (15, 16),
            (12, 17), (12, 18), (12, 19), (12, 20),
            (17, 13), (18, 14), (19, 15), (20, 16)
        )

        sorted_nodes = list(DAG.sort_topologically())

        assert set(sorted_nodes) == set(DAG.nodes)
        for source, target in DAG.edges:
            assert sorted_nodes.index(source) < sorted_nodes.index(target)
