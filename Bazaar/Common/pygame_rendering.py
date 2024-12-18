import math
from pygame import Surface, SRCALPHA, Rect
import pygame.draw
from Bazaar.Common.cards import Card
from Bazaar.Common.pebble_collection import Color, PebbleCollection
from Bazaar.Common.equations import Equation, EquationTable
from pydantic import PositiveInt
from Bazaar.Common.turn_state import TurnState

"""
This module defines a set of static methods to render game objects to Pygame surfaces. Defining
the methods in this way allows the main implementation to remain agnostic of the chosen API.
"""


def color_to_rgb(color: Color) -> tuple[int, int, int, int]:
    """
    Converts the passed in Color to an RGBA value.

    Arguments:
        color (Color): The color to convert.

    Returns:
        The RGBA value associated with the passed in Color.
    """
    match color:
        case Color.RED:
            return 255, 0, 0, 255
        case Color.WHITE:
            return 255, 255, 255, 255
        case Color.BLUE:
            return 0, 0, 255, 255
        case Color.GREEN:
            return 0, 255, 0, 255
        case Color.YELLOW:
            return 255, 255, 0, 255
        case _:
            return 0, 0, 0, 255


def card_to_image(card: Card, width: PositiveInt, height: PositiveInt) -> Surface:
    """
    Renders a card to an image with the given width and height, with the image showing the
    cost of the card and whether it has a face.

    Arguments:
        card (Card): the card to render.
        width (positive int): the width of the resulting image.
        height (positive int): the height of the resulting image.

    Returns:
        A Surface object holding the rendered image of the given card.
    """

    center_size, margin_width, margin_height = _calculate_margins(width, height)

    surface = _draw_margins(width, height, margin_width, margin_height)

    circles_across = 9

    r = center_size / circles_across

    circles = card.cost.as_list_of_colors()

    _draw_circle_of_circles(surface, circles, circles_across, r)

    if card.face:
        _draw_face(surface, r)

    return surface


def equation_to_image(equation: Equation, height: PositiveInt) -> Surface:
    """
    Renders an equation to an image with the given height (with the rest of the image scaled
    appropriately), with the image showing both sides of the equation and indicating their
    equality.

    Arguments:
        equation (Equation): the equation to render.
        height (positive int): the height of the resulting image.

    Returns:
        A Surface object holding the rendered image of the given equation.
    """
    surface = Surface((height * 9, height), flags=SRCALPHA)

    x = 0

    surface.blit(
        pebble_collection_to_image(
            equation.left, height * sum(equation.left.values()), height
        ),
        (0, 0),
    )

    x += sum(equation.left.values())

    font = pygame.font.Font(pygame.font.get_default_font(), int(height))

    equals = font.render("=", True, (255, 255, 255, 255), None)

    surface.blit(
        equals,
        (
            (x + 0.5) * height - equals.get_width() / 2,
            height / 2 - equals.get_height() / 2,
        ),
    )

    x += 1

    surface.blit(
        pebble_collection_to_image(
            equation.right, height * sum(equation.right.values()), height
        ),
        (x * height, 0),
    )

    return surface


def equation_table_to_image(
    table: EquationTable, width: PositiveInt, height: PositiveInt
) -> Surface:
    """
    Renders an equation table to an image with the given width and height, with the image showing
    each of the equations in the table, stacked on each other vertically.

    Arguments:
        table (EquationTable): the equation table to render.
        width (positive int): the width of the resulting image
        height (positive int): the height of the resulting image.

    Returns:
        A Surface object holding the rendered image of the given equation table.
    """
    equations = table.get_equations()
    height_per_equation = min(height / len(equations), width / 9)
    surface = Surface((width, height), flags=SRCALPHA)

    for i in range(len(equations)):
        surface.blit(
            equation_to_image(equations[i], height_per_equation),
            (0, i * height / len(equations)),
        )
    return surface


def turn_state_to_image(
    state: TurnState,
    equation_table: EquationTable,
    width: PositiveInt,
    height: PositiveInt,
):
    """
    Renders the given turn state to an image with the given width and height, showing the ID and score of each player,
    the pebbles available to the active player, the cards available,
    the pebbles in the bank, and the state of the current turn.

    Arguments:
        state (GameState): the game state to render.
        equation_table (EquationTable): the equation table to render.
        width (positive int): the width of the resulting image.
        height (positive int): the height of the resulting image.

    Returns:
        A Surface object holding the rendered image of the given equation table.
    """

    surface = Surface((width, height), flags=SRCALPHA)

    surface.blit(
        players_to_image(
            state.player_ids,
            state.scores,
            [state.wallet] + [PebbleCollection(dict()) for _ in range(len(state.scores) - 1)],
            state.active,
            state.current_player_index,
            width / 2,
            2 * height / 5,
        ),
        (0, 0),
    )
    surface.blit(
        equation_table_to_image(equation_table, width / 2, 2 * height / 5),
        (0, 2 * height / 5),
    )
    surface.blit(
        card_spread_to_image(state.tableau, width / 2, height / 5, 5), (width / 2, 0)
    )
    surface.blit(
        pebble_collection_to_image(
            state.bank, width / 2, height / 5, max_pebbles_per_row=20
        ),
        (width / 2, 4 * height / 5),
    )
    surface.blit(
        pygame.font.Font(pygame.font.get_default_font(), int(height / 20)).render(
            str(state.turn_section), False, (0, 0, 0, 255)
        ),
        (0, 9 * height / 10),
    )
    return surface


def _calculate_margins(
    width: PositiveInt, height: PositiveInt
) -> tuple[PositiveInt, PositiveInt, PositiveInt]:
    center_size = min(width, height)
    margin_width = (width - center_size) / 2
    margin_height = (height - center_size) / 2
    return center_size, margin_width, margin_height


def _draw_margins(
    width: PositiveInt,
    height: PositiveInt,
    margin_width: PositiveInt,
    margin_height: PositiveInt,
) -> Surface:
    surface = Surface((width, height), flags=SRCALPHA)
    surface.fill((64, 224, 208, 255))

    if margin_height > 0:
        pygame.draw.rect(
            surface,
            color=(255, 165, 0, 255),
            rect=Rect(0, 0, width, margin_height),
        )
        pygame.draw.rect(
            surface,
            color=(255, 165, 0, 255),
            rect=Rect(0, height - margin_height, width, margin_height),
        )

    if margin_width > 0:
        pygame.draw.rect(
            surface,
            color=(255, 165, 0, 255),
            rect=Rect(0, 0, margin_width, height),
        )
        pygame.draw.rect(
            surface,
            color=(255, 165, 0, 255),
            rect=Rect(width - margin_width, 0, margin_width, height),
        )
    return surface


def _draw_pebble(
    surface: Surface, color: Color, x: PositiveInt, y: PositiveInt, r: PositiveInt
) -> None:
    pygame.draw.circle(surface, color=(0, 0, 0, 255), center=(x, y), radius=r)
    pygame.draw.circle(surface, color=color_to_rgb(color), center=(x, y), radius=r - 2)


def _draw_face(surface: Surface, r: PositiveInt):
    pygame.draw.circle(
        surface,
        color=(255, 127, 0, 255),
        center=(surface.get_width() / 2, surface.get_height() / 2),
        radius=r * 1.25,
    )


def _draw_circle_of_circles(
    surface: Surface, circles: list[Color], circles_across: PositiveInt, r: PositiveInt
):
    each_angle = 2 * math.pi / len(circles)

    current_angle = -math.pi / 2

    for i in range(len(circles)):
        x = surface.get_width() / 2 + math.cos(current_angle) * r * (
            circles_across / 2 - 2
        )
        y = surface.get_height() / 2 + math.sin(current_angle) * r * (
            circles_across / 2 - 2
        )
        _draw_pebble(surface, circles[i], x, y, r)
        current_angle += each_angle


def card_spread_to_image(
    cards: list[Card],
    width: PositiveInt,
    height: PositiveInt,
    cards_per_row: PositiveInt,
):
    rows = math.ceil(len(cards) / cards_per_row)
    card_width = width / cards_per_row
    card_height = height / rows
    surface = Surface((width, height), flags=SRCALPHA)
    for i in range(len(cards)):
        surface.blit(
            card_to_image(cards[i], card_width, card_height),
            ((i % cards_per_row) * card_width, (i // cards_per_row) * card_height),
        )
    return surface


def pebble_collection_to_image(
    pebble_collection: PebbleCollection,
    width: PositiveInt,
    height: PositiveInt,
    min_pebbles_per_row: PositiveInt = 1,
    max_pebbles_per_row: PositiveInt = 100,
) -> Surface:
    surface = Surface((width, height), flags=SRCALPHA)
    pebbles_per_row = max(
        min(sum(pebble_collection.values()), max_pebbles_per_row), min_pebbles_per_row
    )
    rows = math.ceil(sum(pebble_collection.values()) / pebbles_per_row)
    row_height = height / max(1, rows)
    r = min(width / pebbles_per_row, row_height) / 2

    colors = pebble_collection.as_list_of_colors()

    for i in range(len(colors)):
        color = colors[i]
        _draw_pebble(
            surface,
            color,
            ((i % pebbles_per_row) + 0.5) * width / pebbles_per_row,
            (i // pebbles_per_row + 0.5) * row_height,
            r,
        )
    return surface


def _player_to_image(
    player_id: str,
    score: int,
    pebbles: PebbleCollection,
    active: bool,
    is_active_player: bool,
    width: PositiveInt,
    height: PositiveInt,
):
    surface = Surface((width, height), flags=SRCALPHA)
    font_height = int(min(height / 2, width / 3 / max(len(player_id), len(str(score)))))
    font = pygame.font.Font(pygame.font.get_default_font(), font_height)
    if not active:
        font.strikethrough = True
    surface.blit(
        font.render(player_id, True, (255 if is_active_player else 0, 0, 0, 255)),
        (0, 0),
    )
    surface.blit(font.render(str(score), True, (0, 0, 0, 255)), (0, font_height))
    surface.blit(
        pebble_collection_to_image(
            pebbles,
            2 * width / 3,
            height,
            min_pebbles_per_row=10,
            max_pebbles_per_row=10,
        ),
        (width / 3, 0),
    )
    return surface


def players_to_image(
    player_ids: list[str],
    scores: list[int],
    pebbles: list[PebbleCollection],
    active: list[bool],
    current_player_index: int,
    width: PositiveInt,
    height: PositiveInt,
):
    surface = Surface((width, height), flags=SRCALPHA)
    for i in range(len(player_ids)):
        surface.blit(
            _player_to_image(
                player_ids[i],
                scores[i],
                pebbles[i],
                active[i],
                i == current_player_index,
                width,
                height / len(player_ids),
            ),
            (0, height / len(player_ids) * i),
        )
    return surface
