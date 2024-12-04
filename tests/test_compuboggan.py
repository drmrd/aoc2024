from aoc2024 import compuboggan


def test_eval_day3_conditional_example():
    example_source = 'xmul(2,4)&mul[3,7]!^don\'t()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'
    expected_output = 48

    assert compuboggan.eval(example_source) == expected_output


def test_eval_day3_unconditional_example():
    example_source = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
    expected_output = 161

    assert compuboggan.eval(example_source, command_whitelist=['mul']) == expected_output


def test_parse_purified_day3_example():
    example_instructions = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
    expected_parsed_instructions = [
        ('mul', (2, 4)), ('mul', (5, 5)), ('mul', (11, 8)), ('mul', (8, 5))
    ]

    actual_parsed_instructions = list(
        compuboggan.parse_purified(
            example_instructions
        )
    )
    assert actual_parsed_instructions == expected_parsed_instructions