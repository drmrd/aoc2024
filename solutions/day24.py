import operator
import re
from collections import deque
from collections.abc import Sequence, Callable
from dataclasses import astuple, asdict, dataclass

from aoc2024 import utilities
from aoc2024.graph_theory import DiGraph


@dataclass
class BinaryOperator[T]:
    function: Callable[[T, T], T]
    in_nodes: tuple[str, str]


class ComputationGraph[T]:
    def __init__(
            self,
            input_nodes: Sequence[str],
            output_nodes: Sequence[str],
            transformations: Sequence[
                tuple[Callable[[T, T], T], tuple[str, str], str]
            ]
    ):
        self._inputs = input_nodes
        self._outputs = output_nodes
        self._transformation: dict[str, BinaryOperator[T]] = {
            out: BinaryOperator(func, in_)
            for func, in_, out in transformations
        }
        self._graph: DiGraph[str] = DiGraph(*(
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
            in_nodes = self._transformation[node].in_nodes
            function: Callable[[T, T], T] = self._transformation[node].function
            computed_value[node] = function(*(
                computed_value[in_node] for in_node in in_nodes
            ))
        return dict(
            zip(
                self._outputs, (computed_value[node] for node in self._outputs)
            )
        )


@dataclass
class Gate:
    operator: str
    in_wire1: str
    in_wire2: str
    out_wire: str


@dataclass
class FullAdder:
    # Inputs
    in_wire1: str | None = None
    in_wire2: str | None = None
    carry_in: str | None = None

    # Intermediate State
    sum_precarry: str | None = None
    sum_carry: str | None = None
    carry_intermediate: str | None = None

    # Outputs
    sum: str | None = None
    carry_out: str | None = None


def solve_part_one():
    fruit_monitor_notes = list(utilities.input_lines(year=2024, day=24))
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


def solve_part_two(report_adders=False):
    fruit_monitor_notes = list(utilities.input_lines(year=2024, day=24))
    notes_divider = fruit_monitor_notes.index('')
    gate_pattern = re.compile(
        r'^(?P<in_wire1>\w+) (?P<operator>\w+) '
        r'(?P<in_wire2>\w+) -> (?P<out_wire>\w+)$'
    )
    gates = [
        Gate(**gate_pattern.match(note).groupdict())
        for note in fruit_monitor_notes[notes_divider + 1:]
    ]

    swapped_wires = set()

    adders = deque([create_adder(0, gates)])
    for index in range(1, 45):
        previous_carry_out = adders[-1].carry_out

        adders.append(
            new_adder := create_adder(
                index,
                carry_in=previous_carry_out,
                gates=gates
            )
        )

        if any(value is None for value in astuple(new_adder)):
            try:
                swapped_wires |= repair_adders(adders, gates)
                continue
            except ValueError:
                print(
                    'Failed to repair all adders.',
                    'Report of existing adders follows.',
                    end='\n\n'
                )
                report_adders = True
                break
    if report_adders:
        for index, adder in enumerate(adders):
            print(f'Adder for Bit {index}:')
            print(f'  {'wires in:':<20}', {adder.in_wire1, adder.in_wire2})
            print(f'  {'carry_in:':<20}', adder.carry_in)
            for role, wire in asdict(adder).items():
                if role not in {'in_wire1', 'in_wire2', 'carry_in'}:
                    print(f'  {f'{role}:':<20}', wire)
            print()
    return ','.join(sorted(swapped_wires))


def create_adder(
        index: int,
        gates: list[Gate],
        carry_in: str | None = None,
        adder: FullAdder | None = None
) -> FullAdder:
    if index and carry_in is None:
        raise ValueError(
            'A carry_in wire must be provided for non-initial adders.'
        )
    if adder is None:
        adder = FullAdder(
            in_wire1=io_wire('x', index),
            in_wire2=io_wire('y', index),
            carry_in=carry_in
        )

    inputs = {'in_wire1', 'in_wire2'}
    if not index:
        gate_data = {
            'sum': (inputs, 'XOR'),
            'carry_out': (inputs, 'AND')
        }
    else:
        first_carry_pair = {'carry_in', 'sum_precarry'}
        gate_data = {
            'sum_precarry': (inputs, 'XOR'),
            'sum_carry': (inputs, 'AND'),
            'sum': (first_carry_pair, 'XOR'),
            'carry_intermediate': (first_carry_pair, 'AND'),
            'carry_out': ({'sum_carry', 'carry_intermediate'}, 'OR')
        }

    for out_wire, (in_wire_roles, operator_) in gate_data.items():
        try:
            if getattr(adder, out_wire) is None:
                in_wires = {getattr(adder, role) for role in in_wire_roles}
                setattr(
                    adder, out_wire,
                    find_gate(gates, in_wires, operator_).out_wire
                )
        except ValueError:
            break
    return adder


def io_wire(prefix: str, index: int) -> str:
    return f'{prefix}{index:0>2}'


def find_gate(gates: list[Gate], in_wires: set[str], operator_: str) -> Gate:
    try:
        return next(
            gate for gate in gates
            if (
                {gate.in_wire1, gate.in_wire2} == in_wires
                and gate.operator == operator_
            )
        )
    except StopIteration:
        raise ValueError(
            f'No gate found with in_wires {in_wires} and operator {operator_}.'
        )


def repair_adders(adders: deque[FullAdder], gates):
    last_index = len(adders) - 1
    repairs_by_adder_index = [
        (last_index - 1, fix_swapped_sum_wire),
        (last_index, fix_swapped_sum_wire),
        (last_index, fix_swapped_raw_sum_outputs)
    ]
    swapped_wires = set()
    for index, repair in repairs_by_adder_index:
        if index >= 0:
            swapped_wires |= apply_repair(repair, adders, index, gates)
        if index == last_index:
            if not index or all(
                    wire is not None for wire in astuple(adders[index])
            ):
                return swapped_wires
    raise ValueError


def apply_repair(
        repair: Callable[
            [FullAdder, int], tuple[FullAdder, tuple[str, str]] | None
        ],
        adders: deque[FullAdder],
        index: int,
        gates: list[Gate]
) -> set[str]:
    repaired_adder_data = repair(adders[index], index)
    if repaired_adder_data is None:
        return set()
    repaired_adder, swapped_wire_pair = repaired_adder_data
    adders[index] = create_adder(
        index,
        gates,
        carry_in=None if not index else repaired_adder.carry_in,
        adder=repaired_adder
    )
    for downstream_index in range(index + 1, len(adders)):
        adders[downstream_index] = create_adder(
            downstream_index,
            carry_in=adders[downstream_index - 1].carry_out,
            gates=gates
        )
    return set(swapped_wire_pair)


def fix_swapped_sum_wire(
        adder: FullAdder,
        index: int
) -> tuple[FullAdder, tuple[str, str]] | None:
    if index >= 45:
        return None
    actual_sum = adder.sum
    expected_sum = io_wire('z', index)
    if actual_sum is not None and actual_sum != expected_sum:
        for role, wire in asdict(adder).items():
            if wire == expected_sum:
                setattr(adder, role, actual_sum)
                setattr(adder, 'sum', expected_sum)
                break
        else:
            return None
        return adder, (actual_sum, expected_sum)
    return None

# Callable[[FullAdder, int], tuple[FullAdder, tuple[str, str]] | None]
# Callable[[FullAdder, int], tuple[FullAdder, set[str]] | None]
def fix_swapped_raw_sum_outputs(
        adder: FullAdder, _: int
) -> tuple[FullAdder, tuple[str, str]] | None:
    swapped_roles = 'sum_precarry', 'sum_carry'
    swapped_wires = tuple(getattr(adder, role) for role in swapped_roles)
    if any(wire is None for wire in swapped_wires):
        return None
    for role, swapped_wire in zip(swapped_roles, swapped_wires[::-1]):
        setattr(adder, role, swapped_wire)
    return adder, swapped_wires


# Correct Solutions: 60714423975686 & cgh,frt,pmd,sps,tst,z05,z11,z23
if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())