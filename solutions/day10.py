import sys
from collections import deque

import pygame

from aoc2024 import utilities

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

VIRIDIS_RGB_PALETTE = [
    (68, 1, 84),
    (72, 40, 120),
    (62, 73, 137),
    (49, 104, 142),
    (38, 130, 142),
    (31, 158, 137),
    (53, 183, 121),
    (110, 206, 88),
    (181, 222, 43),
    (253, 231, 37)
]

VISUALIZER_COLORS = {
    'active': {
        'trailhead': {'color': (0, 255, 0), 'bg_color': (0, 255, 0)},
        'default': {'color': (0, 255, 0), 'bg_color': (0, 255, 0)},
        'peak': {'color': (0, 255, 0), 'bg_color': (0, 255, 0)}
    },
    'unvisited': {
        'trailhead': {'color': (0, 255, 0), 'bg_color': (0, 0, 0)},
        'default': {'color': (191, 191, 191), 'bg_color': (0, 0, 0)},
        'peak': {'color': (255, 0, 0), 'bg_color': (0, 0, 0)}
    },
    'to_visit': {
        'trailhead': {'color': (0, 255, 0), 'bg_color': (255, 95, 191)},
        'default': {'color': (191, 191, 191), 'bg_color': (255, 95, 191)},
        'peak': {'color': (255, 0, 0), 'bg_color': (255, 95, 191)}
    },
    'visited': {
        'trailhead': {'color': (0, 255, 0), 'bg_color': (63, 63, 255)},
        'default': {'color': (191, 191, 191), 'bg_color': (63, 63, 255)},
        'peak': {'color': (255, 0, 0), 'bg_color': (63, 63, 255)}
    }
}


def solve_part_one(visualize=False, fps=60):
    return _count_trails(allow_revisiting=False, visualize=visualize, fps=fps)


def solve_part_two(visualize=False, fps=60):
    return _count_trails(allow_revisiting=True, visualize=visualize, fps=fps)


def _count_trails(
        allow_revisiting: bool, visualize: bool = False, fps: int = 60
) -> int:
    topographical_map = utilities.input_grid(year=2024, day=10, caster=int)
    map_shape = len(topographical_map), len(topographical_map[0])
    trailheads = [
        (row, column)
        for row in range(map_shape[0])
        for column in range(map_shape[1])
        if topographical_map[row][column] == 0
    ]

    if visualize:
        visualizer = trail_search_visualizer(topographical_map, fps=fps)
        topographical_map_data = [
            [
                {
                    'height': topographical_map[row][column],
                    'color': (
                        VISUALIZER_COLORS['unvisited']['default']['color']
                    ),
                    'bg_color': (
                        VIRIDIS_RGB_PALETTE[topographical_map[row][column]]
                    )
                }
                for column in range(map_shape[1])
            ]
            for row in range(map_shape[0])
        ]
    else:
        visualizer = infinite_coroutine()
        topographical_map_data = None
    next(visualizer)

    cumulative_rating_or_score = 0
    for trailhead in trailheads:
        trailhead_rating_or_score = 0
        visited = set()
        to_visit = deque([trailhead])
        while to_visit:
            node = to_visit.pop()
            node_height = topographical_map[node[0]][node[1]]
            visited.add(node)
            to_visit.extend((
                neighbor
                for neighbor in _neighbors_at_height(
                    topographical_map, node, node_height + 1, map_shape
                )
                if allow_revisiting or neighbor not in visited
            ))
            update_visualizer_state(
                topographical_map,
                topographical_map_data,
                node,
                visited,
                to_visit
            )
            visualizer.send(topographical_map_data)
            if node_height == 9:
                trailhead_rating_or_score += 1
        cumulative_rating_or_score += trailhead_rating_or_score
    return cumulative_rating_or_score


def _neighbors_at_height(map, node, height, map_shape):
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    row, column = node
    for row_offset, column_offset in neighbor_offsets:
        neighbor_row = row + row_offset
        neighbor_column = column + column_offset
        if (
                (neighbor := (neighbor_row, neighbor_column)) != (row, column)
                and 0 <= neighbor_row < map_shape[0]
                and 0 <= neighbor_column < map_shape[1]
                and map[neighbor_row][neighbor_column] == height
        ):
            yield neighbor


def update_visualizer_state(
        topographical_map,
        topographical_map_data,
        node,
        visited,
        to_visit
):
    if topographical_map_data is None:
        return
    node_type = height_to_node_type(topographical_map[node[0]][node[1]])
    topographical_map_data[node[0]][node[1]]['color'] = (
        VISUALIZER_COLORS['active'][node_type]['color']
    )
    topographical_map_data[node[0]][node[1]]['bg_color'] = (
        VISUALIZER_COLORS['active'][node_type]['bg_color']
    )
    for row, column in to_visit:
        node_type = height_to_node_type(topographical_map[row][column])
        topographical_map_data[row][column]['color'] = (
            VISUALIZER_COLORS['to_visit'][node_type]['color']
        )
        topographical_map_data[row][column]['bg_color'] = (
            VISUALIZER_COLORS['to_visit'][node_type]['bg_color']
        )
    for row, column in visited:
        node_type = height_to_node_type(topographical_map[row][column])
        topographical_map_data[row][column]['color'] = (
            VISUALIZER_COLORS['visited'][node_type]['color']
        )
        topographical_map_data[row][column]['bg_color'] = (
            VISUALIZER_COLORS['visited'][node_type]['bg_color']
        )


def height_to_node_type(height):
    match height:
        case 0:
            return 'trailhead'
        case 9:
            return 'peak'
        case _:
            return 'default'


def trail_search_visualizer(topographical_map, fps=60):
    map_shape = (len(topographical_map), len(topographical_map[0]))
    block_size = 15

    pygame.init()
    screen = pygame.display.set_mode((
        block_size * map_shape[1], block_size * map_shape[0]
    ))
    screen.fill(BLACK)

    clock = pygame.time.Clock()

    def handle_pygame_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_grid(surface: pygame.Surface, topographical_map_data, block_size):
        window_width, window_height = surface.get_size()
        font = pygame.font.SysFont('Arial', block_size)
        for x in range(0, window_width, block_size):
            for y in range(0, window_height, block_size):
                grid_rectangle_data = (
                    topographical_map_data[y // block_size][x // block_size]
                )
                draw_grid_rectangle(
                    x, y,
                    surface=surface,
                    text=str(grid_rectangle_data['height']),
                    font=font,
                    shape=(block_size, block_size),
                    text_color=grid_rectangle_data['color'],
                    background_color=grid_rectangle_data.get(
                        'bg_color',
                        VIRIDIS_RGB_PALETTE[grid_rectangle_data['height']]
                    ),
                    border_color=WHITE,
                    border_width=5
                )
        pygame.display.update()

    def draw_grid_rectangle(
            x, y,
            surface,
            text,
            font,
            shape,
            text_color,
            background_color,
            border_color,
            border_width
    ):
        if isinstance(shape, int):
            shape = (shape, shape)

        pygame.draw.rect(
            surface=surface,
            color=border_color,
            rect=(x, y, shape[0], shape[1]),
            width=border_width
        )
        grid_rectangle = pygame.draw.rect(
            surface=surface,
            color=background_color,
            rect=(x + 1, y + 1, shape[0] - 1, shape[1] - 1)
        )
        rendered_text = font.render(
            text,
            True,
            text_color
        )
        text_rect = rendered_text.get_rect(center=grid_rectangle.center)
        surface.blit(rendered_text, text_rect)

    while True:
        topographical_map_data = yield
        draw_grid(screen, topographical_map_data, 15)
        pygame.display.update()
        handle_pygame_events()
        clock.tick(fps)


def infinite_coroutine(*args, **kwargs):
    while True:
        _ = yield


if __name__ == '__main__':
    # Set a visualize keyword to True to open a visualization in a separate
    # window.
    print('Solution to Part 1:', solve_part_one())
    print('Solution to Part 2:', solve_part_two())