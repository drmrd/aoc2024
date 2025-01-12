from aoc2024 import utilities
from aoc2024.lanternfish_wms import Box, Warehouse, DummyThiccBox, DummyThiccWall


def solve_part_one():
    warehouse_map, roe_bot_routine_lines = (
        '\n'.join(utilities.input_lines(year=2024, day=15))
    ).split('\n\n')
    warehouse = Warehouse.from_lanternfish_printout(
        map_=warehouse_map.split('\n'),
        roe_bot_routine=''.join(roe_bot_routine_lines.split('\n'))
    )
    roe_bot = warehouse.roe_bot

    for direction in roe_bot.routine:
        roe_bot.move(direction)

    boxes = (
        entity
        for row in warehouse.grid
        for entity in row
        if isinstance(entity, Box)
    )
    return sum(box.gps_coordinate for box in boxes)


def solve_part_two():
    warehouse_map, roe_bot_routine_lines = (
        '\n'.join(utilities.input_lines(year=2024, day=15))
    ).split('\n\n')
    warehouse = Warehouse.from_lanternfish_printout(
        map_=warehouse_map.split('\n'),
        roe_bot_routine=''.join(roe_bot_routine_lines.split('\n')),
        passive_entity_types=(DummyThiccWall, DummyThiccBox),
        dummy_thiccen=True
    )
    roe_bot = warehouse.roe_bot

    for direction in roe_bot.routine:
        roe_bot.move(direction)

    boxes = (
        entity
        for row in warehouse.grid
        for entity in row[::2]
        if isinstance(entity, DummyThiccBox)
    )
    return sum(box.gps_coordinate for box in boxes)


if __name__ == '__main__':
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())