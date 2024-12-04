"""
The premier computing platform for Toboggan Rental Warehouse Management
Systems.
"""
import re
from collections.abc import Container, Iterator


def eval(source: str, command_whitelist: Container[str] = frozenset()) -> int:
    def filter_instructions(
            instructions: Iterator[tuple[str, tuple[int, int]]]
    ) -> Iterator[tuple[str, tuple[int, int]]]:
        for instruction in instructions:
            command, _ = instruction
            if not command_whitelist or command in command_whitelist:
                yield instruction

    whitelisted_instructions = filter_instructions(parse_purified(source))
    result = 0
    doing = True
    for command, arguments in whitelisted_instructions:
        match command:
            case 'mul':
                if doing:
                    result += arguments[0] * arguments[1]
            case 'do':
                doing = True
            case 'don\'t':
                doing = False
    return result


def parse_purified(
        corrupted_source: str
) -> Iterator[tuple[str, tuple[int, int]]]:
    instruction_pattern = re.compile(
        r'(?P<command>do|don\'t|mul)\((?P<arguments>(?:\d{1,3},)*(?:\d{1,3})?)\)'
    )
    for match in instruction_pattern.finditer(corrupted_source):
        arguments = match.group('arguments')
        if arguments:
            arguments = tuple(
                int(argument) for argument in arguments.split(',')
            )
        else:
            arguments = tuple()
        yield match.group('command'), arguments