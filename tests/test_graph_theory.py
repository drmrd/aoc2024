import math

import pytest

from aoc2024.graph_theory import DiGraph, UndirectedGraph, grid2d


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
                print(G[edge])
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

    def test_can_add_nodes_to_graph(self, graph_class):
        expected_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)
        ]
        G = graph_class(*expected_edges)
        assert set(G.nodes) == set(range(8))

        G.add_node(8)
        G.add_node(9)

        assert set(G.nodes) == set(range(10))

    def test_can_add_edges_to_graph(self, graph_class):
        expected_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)
        ]
        G = graph_class(*expected_edges)
        initial_nodes = set(G.nodes)
        assert initial_nodes == set(range(8))
        assert set(G.edges) == set(expected_edges)

        for new_edge in [(0, 2), (0, 4), (0, 6), (0, 8)]:
            G.add_edge(new_edge)
            assert set(new_edge).issubset(G.nodes)
            assert new_edge in G.edges

            expected_edges.append(new_edge)
            initial_nodes |= set(new_edge)
            assert set(G.edges) == set(expected_edges)
            assert set(G.nodes) == initial_nodes

            if hasattr(G, 'parents'):
                assert new_edge[0] in G.parents(new_edge[1])
            if hasattr(G, 'children'):
                assert new_edge[1] in G.children(new_edge[0])
            if hasattr(G, 'neighbors'):
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

    def test_can_compute_all_shortest_paths_from_a_source_node(self):
        G = UndirectedGraph(
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
            10: (None, math.inf),
            11: (None, math.inf)
        }
        assert G.shortest_path(0) == expected_distance

        for target in G.nodes:
            assert G.shortest_path(0, target) == expected_distance[target]


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

        path, distance = memory_space.shortest_path_astar(
            source=(0, 0), target=(6, 6), heuristic=taxicab, edge_weight=1
        )
        assert distance == 22