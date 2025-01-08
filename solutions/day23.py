import itertools

from aoc2024 import utilities
from aoc2024.graph_theory import UndirectedGraph


def solve_part_one():
    lan = UndirectedGraph(*(
        line.split('-') for line in utilities.input_lines(day=23)
    ))
    lan_maximal_cliques = lan.cliques()

    chief_historian_pc_candidates = {
        pc for pc in lan.nodes if pc.startswith('t')
    }
    possible_lan_parties = [
        clique
        for clique in lan_maximal_cliques
        if len(clique) >= 3 and clique & chief_historian_pc_candidates
    ]

    return len({
        frozenset((possible_chief, *others))
        for possible_chief in chief_historian_pc_candidates
        for possible_lan_party in possible_lan_parties
        for others in itertools.combinations(
            possible_lan_party - {possible_chief}, 2
        )
        if possible_chief in possible_lan_party
    })


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())