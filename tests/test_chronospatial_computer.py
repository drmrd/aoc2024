from aoc2024.chronospatial_computer import ChronospatialComputer


def test_chronospatial_computer_day17_part1_examples():
    computer = ChronospatialComputer()
    debug_string_template = '\n'.join([
        'Register A: {}',
        'Register B: {}',
        'Register C: {}',
        '',
        'Program: {}'
    ])
    expected_input_output_pairs = [
        (((0, 0, 9), (2, 6)), ((0, 1, 9), tuple())),
        (((10, 0, 0), (5, 0, 5, 1, 5, 4)), ((10, 0, 0), (0, 1, 2))),
        (
            ((2024, 0, 0), (0, 1, 5, 4, 3, 0)),
            ((0, 0, 0), (4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0))
        ),
        (((0, 29, 0), (1, 7)), ((0, 26, 0), tuple())),
        (((0, 2024, 43690), (4, 0)), ((0, 44354, 43690), tuple()))
    ]
    for (
            (initial_registers, program),
            (expected_final_registers, expected_output)
    ) in expected_input_output_pairs:
        computer.load_debug_string(
            debug_string_template.format(
                *initial_registers, ','.join(map(str, program))
            )
        )
        actual_output = computer.run_program()
        assert tuple(computer.register.values()) == expected_final_registers
        assert tuple(actual_output) == expected_output


def test_find_minimal_state_day17_part2_example():
    computer = ChronospatialComputer()
    computer.load_debug_string(
        '\n'.join([
            'Register A: 2024',
            'Register B: 0',
            'Register C: 0',
            '',
            'Program: 0,3,5,4,3,0'
        ])
    )
    assert computer.find_minimal_register_a_state(
        desired_outputs=tuple(computer.program)
    ) == 117_440
