from aoc2024.graph_theory import DiGraph, Graph


def test_graph_can_be_constructed_from_edges():
    expected_nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    expected_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7), (7, 4)
    ]

    G = Graph(*expected_edges)

    assert set(expected_nodes) == set(G.nodes)
    assert set(expected_edges) == set(G.edges)


def test_graph_edges_are_undirected():
    expected_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7), (7, 4)
    ]

    G = Graph(*expected_edges)

    for source, target in expected_edges:
        assert (source, target) in G.edges, (
            f'{(source, target)} not found in G.edges'
        )
        assert (target, source) in G.edges, (
            f'{(source, target)} is in G.edges, but {(target, source)} is not.'
        )


def test_digraph_can_be_constructed_from_edges():
    expected_nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    expected_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7), (7, 4)
    ]

    G = DiGraph(*expected_edges)

    assert set(expected_nodes) == set(G.nodes)
    assert set(expected_edges) == set(G.edges)


def test_digraph_edges_are_directed():
    expected_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7), (7, 4)
    ]

    G = DiGraph(*expected_edges)

    for source, target in expected_edges:
        assert (target, source) not in G.edges, (
            f'Reversed edge {(target, source)} found in G.edges.'
        )


def test_can_retrieve_parents_and_children_of_a_given_node():
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
            f'Node {node} has children {G.children(node)}, not the expected '
            f'children {expected_children}'
        )


def test_dags_can_be_topologically_sorted():
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