import math

import pytest

from aoc2024.graph_theory import DiGraph, UndirectedGraph, grid2d


@pytest.fixture
def karate_club() -> UndirectedGraph[int]:
    return UndirectedGraph(
        (2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 1), (6, 1), (7, 1),
        (7, 5), (7, 6), (8, 1), (8, 2), (8, 3), (8, 4), (9, 1), (9, 3),
        (10, 3), (11, 1), (11, 5), (11, 6), (12, 1), (13, 1), (13, 4), (14, 1),
        (14, 2), (14, 3), (14, 4), (17, 6), (17, 7), (18, 1), (18, 2), (20, 1),
        (20, 2), (22, 1), (22, 2), (26, 24), (26, 25), (28, 3), (28, 24),
        (28, 25), (29, 3), (30, 24), (30, 27), (31, 2), (31, 9), (32, 1),
        (32, 25), (32, 26), (32, 29), (33, 3), (33, 9), (33, 15), (33, 16),
        (33, 19), (33, 21), (33, 23), (33, 24), (33, 30), (33, 31), (33, 32),
        (34, 9), (34, 10), (34, 14), (34, 15), (34, 16), (34, 19), (34, 20),
        (34, 21), (34, 23), (34, 24), (34, 27), (34, 28), (34, 29), (34, 30),
        (34, 31), (34, 32), (34, 33)
    )


@pytest.mark.parametrize(
    'graph_class',
    (UndirectedGraph, DiGraph)
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

    def test_graph_can_be_constructed_with_edge_attributes(self, graph_class):
        expected_edge_data = {
            (0, 1): {'foo': 'bleep', 'bar': 'bloop'},
            (1, 2): {'bar': 'blop', 'baz': 'zeep'}
        }

        G = graph_class(*(
            (*edge, data) for edge, data in expected_edge_data.items()
        ))

        for edge, expected_data in expected_edge_data.items():
            for key, value in expected_data.items():
                assert G[edge][key] == value

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

    def test_nodes_have_in_and_out_edges(self, graph_class):
        G = graph_class(
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6),
            (0, 0), (2, 5), (3, 5)
        )
        if G.is_directed:
            G.add_edge((2, 1))
            G.add_edge((3, 2))
        directed_in_edges = {
            0: {(0, 0), (3, 0)},
            1: {(0, 1), (2, 1)},
            2: {(1, 2), (3, 2)},
            3: {(2, 3)},
            4: {(3, 4)},
            5: {(2, 5), (3, 5), (4, 5)},
            6: {(5, 6)}
        }
        directed_out_edges = {
            0: {(0, 0), (0, 1)},
            1: {(1, 2)},
            2: {(2, 1), (2, 3), (2, 5)},
            3: {(3, 0), (3, 2), (3, 4), (3, 5)},
            4: {(4, 5)},
            5: {(5, 6)},
            6: set()
        }
        for node in G.nodes:
            if G.is_directed:
                assert G.in_edges(node) == directed_in_edges[node]
                assert G.out_edges(node) == directed_out_edges[node]
            else:
                assert G.in_edges(node) == {
                    edge[::-1] for edge in G.out_edges(node)
                }
                assert G.in_edges(node) == (
                    directed_in_edges[node]
                    | {edge[::-1] for edge in directed_out_edges[node]}
                )

    def test_can_add_nodes_to_graph(self, graph_class):
        expected_edges = {
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)
        }
        G = graph_class(*expected_edges)
        assert set(G.nodes) == set(range(8))

        G.add_node(8)
        G.add_node(9)

        assert set(G.nodes) == set(range(10))
        assert set(G.edges) == expected_edges

    def test_can_add_edges_to_graph(self, graph_class):
        initial_edges = {
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)
        }
        G = graph_class(*initial_edges)
        initial_nodes = set(G.nodes)
        assert initial_nodes == set(range(8))
        assert set(G.edges) == set(initial_edges)

        for new_edge in [(0, 2), (0, 4), (0, 6), (0, 8)]:
            G.add_edge(new_edge)
            assert set(new_edge).issubset(G.nodes)
            assert new_edge in G.edges
            if not G.is_directed:
                assert new_edge[::-1] in G.edges

            initial_edges.add(new_edge)
            initial_nodes |= set(new_edge)
            assert set(G.edges) == set(initial_edges)
            assert set(G.nodes) == initial_nodes

            if hasattr(G, 'parents'):
                assert new_edge[0] in G.parents(new_edge[1])
            if hasattr(G, 'children'):
                assert new_edge[1] in G.children(new_edge[0])
            if hasattr(G, 'neighbors'):
                assert new_edge[0] in G.neighbors(new_edge[1])
                assert new_edge[1] in G.neighbors(new_edge[0])

        assert set(G.nodes) == set(range(9))

    def test_can_remove_nodes_from_graph(self, graph_class):
        initial_edges = {
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7),
            (0, 2), (0, 4), (0, 6), (0, 8)
        }
        G = graph_class(*initial_edges)

        G.remove_node(0)
        expected_remaining_nodes = set(range(1, 9))
        expected_remaining_edges = {
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)
        }
        assert set(G.nodes) == expected_remaining_nodes
        assert set(G.edges) == expected_remaining_edges

        for node in expected_remaining_nodes:
            if hasattr(G, 'parents'):
                assert 0 not in G.parents(node)
            if hasattr(G, 'children'):
                assert 0 not in G.children(node)
            if hasattr(G, 'neighbors'):
                assert 0 not in G.neighbors(node)

    def test_can_remove_edges_from_graph(self, graph_class):
        remaining_edges = {
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7),
            (0, 2), (0, 4), (0, 6), (0, 8)
        }
        G = graph_class(*remaining_edges)
        initial_nodes = set(G.nodes)
        assert initial_nodes == set(range(9))
        assert set(G.edges) == set(remaining_edges)

        for deleted_edge in [(0, 2), (0, 4), (0, 6), (0, 8)]:
            G.remove_edge(deleted_edge)
            remaining_edges.remove(deleted_edge)
            assert deleted_edge not in G.edges
            assert set(G.edges) == remaining_edges
            assert set(G.nodes) == initial_nodes

    def test_can_compute_all_shortest_paths_from_a_source_node(self, graph_class):
        G = graph_class(
            (0, 1, 5), (1, 2, 3), (2, 3, 7), (3, 4, 5),
            (0, 2, 7), (0, 4, 10),
            (10, 11, 1)
        )

        expected_distance = {
            0: ([[0]], 0),
            1: ([[0, 1]], 5),
            2: ([[0, 2]], 7),
            3: ([[0, 2, 3]], 14),
            4: ([[0, 4]], 10),
            10: ([], math.inf),
            11: ([], math.inf)
        }
        assert G.all_shortest_paths(0) == expected_distance

        for target in G.nodes:
            assert G.all_shortest_paths(0, target) == expected_distance[target]

    def test_can_compute_a_shortest_path_from_a_source_to_a_target(self, graph_class):
        G = graph_class(
            (0, 1, 5), (1, 2, 3), (2, 3, 7), (3, 4, 5),
            (0, 2, 7), (0, 4, 10),
            (10, 11, 1)
        )

        expected_distance = {
            0: ([0], 0),
            1: ([0, 1], 5),
            2: ([0, 2], 7),
            3: ([0, 2, 3], 14),
            4: ([0, 4], 10)
        }
        for target, (expected_path, expected_distance) in expected_distance.items():
            actual_path, actual_distance = G.shortest_path(0, target, lambda p1, p2: 0)
            assert actual_path == expected_path
            assert actual_distance == expected_distance

    def test_shortest_path_raises_error_if_source_is_not_an_ancestor_of_target(self, graph_class):
        G = graph_class(
            (0, 1, 5), (1, 2, 3), (2, 3, 7), (3, 4, 5),
            (0, 2, 7), (0, 4, 10),
            (10, 11, 1)
        )
        with pytest.raises(ValueError, match='Unable to find a path'):
            G.shortest_path(0, 10, lambda p1, p2: 0)


class TestGraph:
    def test_can_retrieve_neighbors_of_a_given_node(self):
        G = UndirectedGraph((0, 1), (1, 2), (2, 3), (3, 4), (3, 0), (0, 2), (0, 4))
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

    def test_can_find_all_maximal_cliques(self, karate_club):
        expected_clique_membership = {
            1: 13, 2: 6, 3: 7, 4: 3, 5: 2, 6: 3, 7: 3, 8: 1, 9: 3, 10: 2, 11: 2,
            12: 1, 13: 1, 14: 2, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 2,
            21: 1, 22: 1, 23: 1, 24: 3, 25: 2, 26: 2, 27: 1, 28: 3, 29: 2,
            30: 2, 31: 2, 32: 4, 33: 9, 34: 14
        }

        actual_cliques = karate_club.cliques()

        actual_clique_membership = {
            node: sum(node in clique for clique in actual_cliques)
            for node in karate_club.nodes
        }
        assert actual_clique_membership == expected_clique_membership


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


class TestGraphConstructors:
    def test_grid2d_creates_2d_grid_of_given_shape(self):
        shape = (2, 3)
        expected_edges = {
            ((0, 0), (0, 1)), ((0, 1), (0, 2)),
            ((0, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2)),
            ((1, 0), (1, 1)), ((1, 1), (1, 2))
        }

        expected_grid = UndirectedGraph(*expected_edges)

        actual_grid = grid2d(*shape)
        assert set(actual_grid.nodes) == set(expected_grid.nodes)
        assert set(actual_grid.edges) == set(expected_grid.edges)

    def test_day18_part1_example1(self):
        pushed_bytes = '\n'.join([
            '5,4', '4,2', '4,5', '3,0', '2,1', '6,3', '2,4', '1,5', '0,6',
            '3,3', '2,6', '5,1', '1,2', '5,5', '2,5', '6,5', '1,4', '0,4',
            '6,4', '1,1', '6,1', '1,0', '0,5', '1,6', '2,0'
        ])

        memory_space = grid2d(7, 7)
        for pushed_byte in pushed_bytes.split('\n')[:12]:
            grid_node = tuple(map(int, pushed_byte.split(',')))[::-1]
            memory_space.remove_node(grid_node)

        def taxicab(node1, node2):
            if len(node1) != len(node2):
                raise ValueError(
                    f'Dimension mismatch between nodes {node1} and {node2}.'
                )
            return sum(
                abs(entry1 - entry2)
                for entry1, entry2 in zip(node1, node2)
            )

        path, distance = memory_space.shortest_path(
            source=(0, 0), target=(6, 6), heuristic=taxicab, edge_weight=1
        )
        assert distance == 22