import operator
import re
from collections.abc import Sequence, Callable

from aoc2024 import utilities
from aoc2024.graph_theory import DiGraph


class ComputationGraph[T]:
    def __init__(
            self,
            input_nodes: Sequence[str],
            output_nodes: Sequence[str],
            transformations: Sequence[
                tuple[Callable[[...], T], Sequence[str], str]
            ]
    ):
        self._inputs = input_nodes
        self._outputs = output_nodes
        self._transformation = {
            out: {'function': func, 'in_nodes': in_}
            for func, in_, out in transformations
        }
        self._graph = DiGraph(*(
                (in_node, out_node)
                for _, in_nodes, out_node in transformations
                for in_node in in_nodes
        ))
        orphans = {
            node for node in self._graph.nodes if not self._graph.parents(node)
        }
        if orphans != set(self._inputs):
            raise ValueError(
                'The input nodes must be the only parentless nodes in the '
                'computation graph.'
            )
        if not set(self._inputs) < set(self._graph.nodes):
            raise ValueError(
                'At least one input node not found in the given '
                'transformations.'
            )
        if not set(self._outputs) < set(self._graph.nodes):
            raise ValueError(
                'At least one output node not found in the given '
                'transformations.'
            )

    def __call__(self, *args: T):
        if len(args) != (total_inputs := len(self._inputs)):
            raise ValueError(
                f'Exactly {total_inputs} must be provided to this computation '
                'graph.'
            )
        computed_value = {
            input_node: value
            for input_node, value in zip(self._inputs, args)
        }
        uncomputed_nodes = [
            node
            for node in self._graph.sort_topologically()
            if node not in self._inputs
        ]
        for node in uncomputed_nodes:
            in_nodes = self._transformation[node]['in_nodes']
            function = self._transformation[node]['function']
            computed_value[node] = function(*(
                computed_value[in_node] for in_node in in_nodes
            ))
        return dict(
            zip(
                self._outputs, (computed_value[node] for node in self._outputs)
            )
        )


def solve_part_one():
    fruit_monitor_notes = list(utilities.input_lines(day=24))
    notes_divider = fruit_monitor_notes.index('')
    system_inputs = {
        wire: int(value)
        for wire, value in map(
            lambda note: note.split(': '),
            fruit_monitor_notes[:notes_divider]
        )
    }
    gate_operator = {
        'AND': operator.and_,
        'OR': operator.or_,
        'XOR': operator.xor
    }
    gate_pattern = re.compile(
        r'^(?P<in_wire1>\w+) (?P<gate_name>\w+) '
        r'(?P<in_wire2>\w+) -> (?P<out_wire>\w+)$'
    )
    gate_matches = [
        gate_pattern.match(note)
        for note in fruit_monitor_notes[notes_divider + 1:]
    ]
    system_outputs = sorted(
        out_wire
        for gate_match in gate_matches
        if (out_wire := gate_match.group('out_wire')).startswith('z')
    )
    transformations = [
        (
            gate_operator[gate_match.group('gate_name')],
            (gate_match.group('in_wire1'), gate_match.group('in_wire2')),
            gate_match.group('out_wire')
        )
        for gate_match in gate_matches
    ]
    output = ComputationGraph(
        input_nodes=list(system_inputs),
        output_nodes=system_outputs,
        transformations=transformations
    )(*system_inputs.values())

    return int(''.join(map(str, reversed(output.values()))), 2)


def solve_part_two():
    return 'TBD'


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())