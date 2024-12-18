from Bazaar.Common.equations import EquationTable
from Bazaar.Referee.game_state import GameState
from pydantic import PositiveInt
from pygame import Surface, SRCALPHA
import pygame
from Bazaar.Common.pygame_rendering import (
    players_to_image,
    equation_table_to_image,
    card_spread_to_image,
    pebble_collection_to_image,
)


def game_state_to_image(state: GameState, width: PositiveInt, height: PositiveInt) -> Surface:
    """
    Renders the given game state to an image with the given width and height, showing the ID, score, and
    pebbles of each player, the cards available, the cards in the deck, the pebbles in the bank, and the
    state of the current turn.

    Arguments:
        state (GameState): the game state to render.
        width (positive int): the width of the resulting image.
        height (positive int): the height of the resulting image.

    Returns:
        A Surface object holding the rendered image of the given equation table.
    """

    surface = Surface((width, height), flags=SRCALPHA)
    players = state.players
    surface.blit(
        players_to_image(
            [p.player_id for p in players],
            [p.score for p in players],
            [p.wallet for p in players],
            [p.active for p in players],
            state.current_player_index,
            width / 2,
            2 * height / 5,
        ),
        (0, 0),
    )
    surface.blit(
        equation_table_to_image(EquationTable(state.list_of_equations), width / 2, 2 * height / 5),
        (0, 2 * height / 5),
    )
    surface.blit(
        card_spread_to_image(state.tableau, width / 2, height / 5, 5), (width / 2, 0)
    )
    surface.blit(
        card_spread_to_image(state.deck, width / 2, 2 * height / 5, 10),
        (width / 2, height / 5),
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
