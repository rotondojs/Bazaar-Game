import random

import collections
import pygame

from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.pebble_collection import Color, PebbleCollection
from Bazaar.Common.pygame_rendering import turn_state_to_image
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.pygame_rendering import game_state_to_image

pygame.init()
screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("Bazaar")


def generate_valid_equation():
    left_colors = random.sample(list(Color), k=2)
    right_colors = random.sample([c for c in Color if c not in left_colors], k=2)

    left_pebbles = collections.defaultdict(int)
    right_pebbles = collections.defaultdict(int)

    for i in range(random.randint(1, 4)):
        left_pebbles[random.choice(left_colors)] += 1

    for i in range(random.randint(1, 4)):
        right_pebbles[random.choice(right_colors)] += 1

    return Equation(
        PebbleCollection(dict(left_pebbles)), PebbleCollection(dict(right_pebbles))
    )


def generate_random_card():
    colors = collections.defaultdict(int)

    for i in range(5):
        colors[random.choice(list(Color))] += 1
    face = random.choice([True, False])

    return Card(PebbleCollection(dict(colors)), face)


table = EquationTable([generate_valid_equation() for _ in range(10)])

deck = [generate_random_card() for _ in range(30)]

tableau = [generate_random_card() for _ in range(5)]

bank = PebbleCollection(
    {Color.RED: 20, Color.BLUE: 20, Color.GREEN: 20, Color.WHITE: 20, Color.YELLOW: 20}
)

players = [
    GamePlayer(
        pebbles=PebbleCollection({}),
        score=0,
        active=True,
    )
    for i in range(random.randrange(1, 8))
]

game_state = GameState(
    table,
    deck,
    tableau,
    bank,
    players,
    0,
    TurnSection.START_OF_TURN,
)

selected_index = 0
reverse = False
global_state = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                game_state.get_pebble()
            if event.key == pygame.K_0:
                selected_index = 10
            if event.key == pygame.K_1:
                selected_index = 1
            if event.key == pygame.K_2:
                selected_index = 2
            if event.key == pygame.K_3:
                selected_index = 3
            if event.key == pygame.K_4:
                selected_index = 4
            if event.key == pygame.K_5:
                selected_index = 5
            if event.key == pygame.K_6:
                selected_index = 6
            if event.key == pygame.K_7:
                selected_index = 7
            if event.key == pygame.K_8:
                selected_index = 8
            if event.key == pygame.K_9:
                selected_index = 9
            if event.key == pygame.K_r:
                reverse = not reverse
            if event.key == pygame.K_e:
                game_state.use_equation(selected_index - 1, not reverse)
                reverse = False
            if event.key == pygame.K_p:
                game_state.purchase_card(selected_index - 1)
            if event.key == pygame.K_n:
                game_state.end_turn()
            if event.key == pygame.K_k:
                game_state.kick_player(selected_index - 1)
            if event.key == pygame.K_SPACE:
                global_state = not global_state

    screen.fill((127, 127, 127, 255))

    if global_state:
        screen.blit(
            game_state_to_image(game_state, screen.get_width(), screen.get_height()),
            (0, 0),
        )
    else:
        screen.blit(
            turn_state_to_image(
                game_state.get_repr_for_current_player(),
                table,
                screen.get_width(),
                screen.get_height(),
            ),
            (0, 0),
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
