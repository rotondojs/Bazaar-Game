import unittest

from Bazaar.Common.equations import EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction, ActionType
from Bazaar.Player.strategy import Strategy


class MockStrategy(Strategy):
    def request_pebble_or_trades(
        self, state: TurnState, equation_table: EquationTable
    ) -> list[PlayerAction]:
        return [PlayerAction(ActionType.GET_PEBBLE)]

    def request_cards(self, state: TurnState) -> list[PlayerAction]:
        return [PlayerAction(ActionType.PURCHASE_CARD, index=0)]


class MockTurnState(TurnState):
    pass


class TestPlayerMechanism(unittest.TestCase):

    def setUp(self):
        self.mock_strategy = MockStrategy(
            equation_search_depth=0, value_function=lambda x: 0
        )
        self.mock_turn_state = MockTurnState()

        self.player_mechanism = PlayerMechanism(
            player_name="TestPlayer", strategy=self.mock_strategy
        )

    def test_initialization(self):
        self.assertEqual(self.player_mechanism.player_name, "TestPlayer")
        self.assertEqual(self.player_mechanism.strategy, self.mock_strategy)
        self.assertIsInstance(self.player_mechanism.equation_table, EquationTable)

    def test_setup(self):
        mock_equation_table = EquationTable([])
        self.player_mechanism.setup(mock_equation_table)
        self.assertEqual(self.player_mechanism.equation_table, mock_equation_table)

    def test_name_method(self):
        self.assertEqual(self.player_mechanism.name(), "TestPlayer")

    def test_request_pebble_or_trades(self):
        actions = self.player_mechanism.request_pebble_or_trades(self.mock_turn_state)

        expected_actions = [PlayerAction(ActionType.GET_PEBBLE)]
        self.assertEqual(actions, expected_actions)

    def test_request_cards(self):
        actions = self.player_mechanism.request_cards(self.mock_turn_state)

        expected_actions = [PlayerAction(ActionType.PURCHASE_CARD, index=0)]
        self.assertEqual(actions, expected_actions)

    def test_win_method(self):
        try:
            self.player_mechanism.win(True)
            self.player_mechanism.win(False)
            success = True
        except BazaarException as _:
            success = False

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
