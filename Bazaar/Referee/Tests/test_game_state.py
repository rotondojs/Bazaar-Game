import random
import unittest

from Bazaar.Referee.game_state import GameState
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.cards import Card
from Bazaar.Common.pebble_collection import PebbleCollection, Color
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.turn_state import TurnState
from Bazaar.Common.exceptions import BazaarException


class TestGameState(unittest.TestCase):
    def setUp(self):

        random.seed(42)

        self.table = EquationTable(
            [
                Equation(
                    PebbleCollection({Color.RED: 1}), PebbleCollection({Color.BLUE: 1})
                ),
                Equation(
                    PebbleCollection({Color.BLUE: 2}),
                    PebbleCollection({Color.GREEN: 1}),
                ),
                Equation(
                    PebbleCollection({Color.GREEN: 3}),
                    PebbleCollection({Color.RED: 1}),
                ),
            ]
        )

        self.deck = [
            Card(
                cost=PebbleCollection({Color.RED: 2, Color.BLUE: 2, Color.GREEN: 1}),
                face=True,
            ),
            Card(
                cost=PebbleCollection({Color.RED: 1, Color.BLUE: 3, Color.GREEN: 1}),
                face=False,
            ),
        ]

        self.tableau = [
            Card(cost=PebbleCollection({Color.RED: 4, Color.BLUE: 1}), face=True),
            Card(cost=PebbleCollection({Color.BLUE: 3, Color.GREEN: 2}), face=False),
        ]

        self.bank = PebbleCollection({Color.RED: 10, Color.BLUE: 10, Color.GREEN: 10})

        self.players = [
            GamePlayer(
                pebbles=PebbleCollection({Color.RED: 2, Color.BLUE: 2, Color.GREEN: 1}),
                score=0,
                active=True,
            ),
            GamePlayer(
                pebbles=PebbleCollection({Color.BLUE: 1, Color.GREEN: 1}),
                score=0,
                active=True,
            ),
            GamePlayer(
                pebbles=PebbleCollection({Color.BLUE: 10, Color.RED: 10}),
                score=0,
                active=True,
            ),
        ]

        self.game_state = GameState(
            self.table,
            self.deck,
            self.tableau,
            self.bank,
            self.players,
            0,
            TurnSection.START_OF_TURN,
        )

    def test_get_current_player(self):
        self.assertEqual(self.game_state.get_current_player(), self.players[0])

    def test_get_repr_for_current_player(self):
        self.assertEqual(
            self.game_state.get_repr_for_current_player(),
            TurnState(
                tableau=self.tableau,
                bank=self.bank,
                scores=[0, 0, 0],
                player=self.players[0]
            ),
        )

    def test_end_turn_valid(self):
        self.game_state._turn_section = TurnSection.MAKING_EXCHANGES

        self.assertEqual(
            self.game_state._turn_section,
            TurnSection.MAKING_EXCHANGES,
        )

        self.assertEqual(self.game_state._current_player_index, 0)

        self.game_state.end_turn()

        self.assertEqual(
            self.game_state._turn_section,
            TurnSection.START_OF_TURN,
        )

        self.assertEqual(self.game_state._current_player_index, 1)

    def test_end_turn_wrap_around(self):
        self.game_state._current_player_index = 2

        self.assertEqual(self.game_state._current_player_index, 2)

        self.game_state.end_turn()

        self.assertEqual(self.game_state._current_player_index, 0)

        self.assertEqual(
            self.game_state._turn_section,
            TurnSection.START_OF_TURN,
        )

    def test_kick_player_valid(self):
        self.assertTrue(self.game_state._players[0].active)

        self.game_state.kick_player(0)

        self.assertFalse(self.game_state._players[0].active)

    def test_kick_player_invalid_index(self):
        with self.assertRaises(BazaarException):
            self.game_state.kick_player(3)

    def test_kick_player_calls_end_turn(self):
        self.game_state._current_player_index = 0
        self.game_state._turn_section = TurnSection.MAKING_EXCHANGES

        self.assertEqual(self.game_state._current_player_index, 0)

        self.assertEqual(
            self.game_state._turn_section,
            TurnSection.MAKING_EXCHANGES,
        )

        self.game_state.kick_player(0)

        self.assertEqual(self.game_state._current_player_index, 1)

        self.assertEqual(
            self.game_state._turn_section,
            TurnSection.START_OF_TURN,
        )


if __name__ == "__main__":
    unittest.main()
