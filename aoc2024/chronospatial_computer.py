from collections import deque
from collections.abc import Callable, Mapping
from copy import deepcopy
from typing import Generator


class ChronospatialComputer:
    def __init__(self, registers: tuple[int, int, int] = (0, 0, 0)):
        self._initial_register = dict(zip(('a', 'b', 'c'), registers))
        self._register = deepcopy(self._initial_register)
        self._instruction = dict(
            zip(
                range(8),
                [
                    self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out,
                    self.bdv, self.cdv
                ]
            )
        )
        self._pointer = 0
        self._program = None
        self._program_length = None
        self._outputs: deque[int] = deque()

    @property
    def register(self):
        return deepcopy(self._register)

    @property
    def program(self):
        return self._program

    def update_register(self, name: str, value: int):
        if name not in self._register:
            raise KeyError(f'Unknown register {name}.')
        self._register[name] = value

    def run_program(
            self,
            halt_condition: Callable[[Mapping[str, int], deque[int]], bool] = (
                lambda _, __: False
            )
    ) -> tuple[int, ...]:
        while (
                (0 <= self._pointer < self._program_length - 1)
                and not halt_condition(self._register, self._outputs)
        ):
            opcode, operand = (
                self._program[self._pointer:self._pointer + 2]
            )
            self._instruction[opcode](operand)  # type: ignore
            self._pointer += 2
        return tuple(self._outputs)

    def outputs_iter(self) -> Generator[int]:
        while 0 <= self._pointer < self._program_length - 1:
            opcode, operand = (
                self._program[self._pointer:self._pointer + 2]
            )
            self._instruction[opcode](operand)  # type: ignore
            if opcode == 5:
                yield self._outputs[-1]
            self._pointer += 2

    def reset(self):
        self._register = deepcopy(self._initial_register)
        self._pointer = 0
        self._outputs = deque()

    def find_minimal_register_a_state(
            self,
            desired_outputs: tuple[int],
            partial_a: int = 0
    ) -> int | None:
        if not desired_outputs:
            return partial_a

        *leading_outputs, trailing_output = desired_outputs
        for candidate_a in range(1 << 10):
            has_consistent_partial_overlap = (
                (candidate_a >> 3) == (partial_a & 0b1111111)
            )
            if has_consistent_partial_overlap:
                self.reset()
                self.update_register('a', candidate_a)
                candidate_first_output = next(self.outputs_iter())
                if candidate_first_output == trailing_output:
                    updated_partial_a = self.find_minimal_register_a_state(
                        leading_outputs,
                        (partial_a << 3) | (candidate_a & 0b111)
                    )
                    if updated_partial_a is not None:
                        return updated_partial_a

    def load_program(
            self, registers: tuple[int, int, int], program: tuple[int]
    ):
        self._initial_register = dict(zip(('a', 'b', 'c'), registers))
        self._register = deepcopy(self._initial_register)
        self._program = program
        self._program_length = len(program)
        self._pointer = 0
        self._outputs = deque()

    def load_debug_string(self, debug_string: str):
        register_lines, program_line = debug_string.split('\n\n')
        register_values = tuple(
            int(register_line.rsplit(' ', maxsplit=1)[1])
            for register_line in register_lines.split('\n')
        )
        program = tuple(
            int(number)
            for number in program_line.rsplit(' ', maxsplit=1)[1]
                                      .split(',')
        )
        self.load_program(register_values, program)  # type: ignore

    def adv(self, operand):
        self._register['a'] //= 2 ** self._combo_op(operand)

    def bxl(self, operand):
        self._register['b'] ^= operand

    def bst(self, operand):
        self._register['b'] = self._combo_op(operand) % 8

    def jnz(self, operand):
        if not self._register['a']:
            return
        else:
            self._pointer = operand - 2

    def bxc(self, operand):
        self._register['b'] ^= self._register['c']

    def out(self, operand):
        self._outputs.append(self._combo_op(operand) % 8)

    def bdv(self, operand):
        self._register['b'] = (
            self._register['a'] // 2 ** self._combo_op(operand)
        )

    def cdv(self, operand):
        self._register['c'] = (
            self._register['a'] // 2 ** self._combo_op(operand)
        )

    def _combo_op(self, operand):
        if 0 <= operand < 4:
            return operand
        elif operand < 7:
            return self._register[chr(operand + 93)]
        else:
            raise ValueError('Combo operand outside defined range 0 to 6.')
