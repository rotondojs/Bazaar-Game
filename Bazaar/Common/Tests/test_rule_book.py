import unittest

from pydantic import ValidationError

from Bazaar.Common.cards import Card
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.turn_state import TurnState
from Bazaar.Common.pebble_collection import Color, PebbleCollection
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.rule_book import RuleBook
from Bazaar.Player.player_action import ActionType, PlayerAction


class TestRuleBook(unittest.TestCase):
    def setUp(self):
        self.equation_table = EquationTable(
            equations=[
                Equation(
                    PebbleCollection({Color.RED: 1}), PebbleCollection({Color.BLUE: 1})
                ),
                Equation(
                    PebbleCollection({Color.BLUE: 2}),
                    PebbleCollection({Color.GREEN: 1}),
                ),
                Equation(
                    PebbleCollection({Color.GREEN: 3}), PebbleCollection({Color.RED: 1})
                ),
                Equation(
                    PebbleCollection({Color.YELLOW: 3}),
                    PebbleCollection({Color.RED: 1}),
                ),
            ]
        )

        self.deck_size = 10

        self.tableau = [
            Card(cost=PebbleCollection({Color.RED: 4, Color.BLUE: 1}), face=True),
            Card(cost=PebbleCollection({Color.YELLOW: 5}), face=True),
            Card(cost=PebbleCollection({Color.BLUE: 3, Color.GREEN: 2}), face=False),
            Card(cost=PebbleCollection({Color.BLUE: 5}), face=True),
        ]

        self.bank = PebbleCollection({Color.RED: 10, Color.BLUE: 10, Color.GREEN: 10})

        self.players = [
            GamePlayer(
                pebbles=PebbleCollection(
                    {Color.RED: 4, Color.BLUE: 1, Color.YELLOW: 5}
                ),
                score=0,
                active=True,
            ),
            GamePlayer(
                pebbles=PebbleCollection({Color.BLUE: 5, Color.GREEN: 1}),
                score=0,
                active=True,
            ),
        ]

        self.scores = [player.score for player in self.players]
        self.active = [player.active for player in self.players]

        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.turn_section = TurnSection.START_OF_TURN

        self.turn_state = TurnState(
            tableau=self.tableau,
            bank=self.bank,
            scores=self.scores,
            player=self.players[0]
        )

    def test_can_get_pebble(self):
        self.assertTrue(
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.GET_PEBBLE),
                self.turn_section
            )
        )

        self.turn_section = TurnSection.MAKING_EXCHANGES
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.GET_PEBBLE),
                self.turn_section
            )

        self.turn_section = TurnSection.PURCHASING_CARDS
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.GET_PEBBLE),
                self.turn_section
            )

        self.turn_section = TurnSection.START_OF_TURN
        self._update_turn_state()

        self.assertTrue(
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.GET_PEBBLE),
                self.turn_section
            )
        )

    def test_can_get_pebble_invalid_actions(self):
        with self.assertRaises(ValidationError):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.PURCHASE_CARD),
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.PURCHASE_CARD, index=3),
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=2, right_to_left=False),
                self.turn_section
            )

    def test_can_get_pebble_or_exchange_invalid_turn_section(self):
        self.turn_section = TurnSection.PURCHASING_CARDS
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                self.turn_section
            )

    def test_can_use_equation_valid_actions(self):
        print(self.turn_section)
        self.assertTrue(
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                self.turn_section
            )
        )

        self.assertTrue(
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                self.turn_section
            )
        )

        self.turn_section = TurnSection.MAKING_EXCHANGES
        self._update_turn_state()

        self.assertTrue(
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=3, right_to_left=False),
                self.turn_section
            )
        )

    def test_can_use_equation_invalid_actions(self):
        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=1, right_to_left=True),
                self.turn_section
            )

        self.turn_section = TurnSection.MAKING_EXCHANGES
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.GET_PEBBLE),
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_get_pebble_or_exchange(
                self.turn_state,
                self.equation_table,
                PlayerAction(ActionType.USE_EQUATION, index=4, right_to_left=True),
                self.turn_section
            )

    def test_can_purchase_cards_valid_turn_state(self):
        self.turn_section = TurnSection.PURCHASING_CARDS
        self._update_turn_state()

        self.assertTrue(
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=0), self.turn_state,
                self.turn_section
            )
        )

        self.turn_section = TurnSection.PURCHASING_CARDS
        self._update_turn_state()

        self.assertTrue(
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=1), self.turn_state,
                self.turn_section
            )
        )

    def test_can_purchase_cards(self):
        self.turn_section = TurnSection.PURCHASING_CARDS
        self._update_turn_state()

        self.assertTrue(
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
                self.turn_state,
                self.turn_section
            )
        )

        self.assertTrue(
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                self.turn_state,
                self.turn_section
            )
        )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=2),
                self.turn_state,
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=2),
                self.turn_state,
                self.turn_section
            )

        self.current_player_index = 1
        self.current_player = self.players[self.current_player_index]
        self._update_turn_state()

        self.assertTrue(
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=3),
                self.turn_state,
                self.turn_section
            )
        )

    def test_can_purchase_cards_invalid_index(self):
        self.turn_section = TurnSection.PURCHASING_CARDS
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=4),
                self.turn_state,
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=-1),
                self.turn_state,
                self.turn_section
            )

        self.current_player_index = 1
        self.current_player = self.players[self.current_player_index]
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
                self.turn_state,
                self.turn_section
            )

    def test_can_purchase_cards_invalid_turn_state(self):
        self.turn_section = TurnSection.START_OF_TURN
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                self.turn_state,
                self.turn_section
            )

    def test_can_purchase_cards_invalid_action(self):
        self.turn_section = TurnSection.MAKING_EXCHANGES
        self._update_turn_state()

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                self.turn_state,
                self.turn_section
            )

        with self.assertRaises(BazaarException):
            RuleBook.attempt_purchase_card(
                PlayerAction(ActionType.GET_PEBBLE),
                self.turn_state,
                self.turn_section
            )

    def _update_turn_state(self):
        self.turn_state = TurnState(
            tableau=self.tableau,
            bank=self.bank,
            scores=self.scores,
            player=self.players[self.current_player_index]
        )


if __name__ == "__main__":
    unittest.main()
