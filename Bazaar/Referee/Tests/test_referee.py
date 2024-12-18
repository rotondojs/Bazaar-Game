import asyncio
import unittest

from Bazaar.Common.scoring import ScoringType
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.strategy import Strategy
from Bazaar.Referee.Tests.mocks.invalid_mechanism import InvalidMechanism
from Bazaar.Referee.Tests.mocks.invalid_move import InvalidMoveMechanism
from Bazaar.Referee.Tests.mocks.mock_mechanism import MockMechanism
from Bazaar.Referee.game_state_factory import GameStateFactory
from Bazaar.Referee.referee import Referee


class TestReferee(unittest.TestCase):
    def setUp(self) -> None: ...

    def test_referee_returns_misbehaved_appropriately(self):
        referee = Referee([MockMechanism(), MockMechanism()], ScoringType.NORMAL)

        self.assertEqual(([], ["MOCK", "MOCK"]), asyncio.run(referee.play()))

    def test_referee_returns_misbehaved_appropriately_invalid_return_type(self):
        referee = Referee([InvalidMechanism(), InvalidMechanism()], ScoringType.NORMAL)

        self.assertEqual(([], ["MOCK", "MOCK"]), asyncio.run(referee.play()))

    def test_referee_returns_misbehaved_appropriately_invalid_move(self):
        referee = Referee([InvalidMoveMechanism(), InvalidMoveMechanism()], ScoringType.NORMAL)

        self.assertEqual(([], ["MOCK", "MOCK"]), asyncio.run(referee.play()))

    def test_referee_returns_correct_winners_passed_in_game_state(self):
        game_state = GameStateFactory(
            seed=41,
            visible_card_count=4,
            deck_card_count=160,
            total_bank_pebbles=1000,
            card_pebble_count=5,
            num_equations=10,
            equation_lower_bound=1,
            equation_upper_bound=4,
            player_count=2,
        ).create()

        scoring = ScoringType.NORMAL

        referee = Referee(
            players=[
                PlayerMechanism(
                    "Alice",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
                PlayerMechanism(
                    "Bob",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
            ],
            scoring=scoring,
            game_state=game_state,
        )

        self.assertEqual((["Alice"], []), asyncio.run(referee.play()))

    def test_referee_returns_correct_winners_passed_no_winner_or_misbehaved(self):
        game_state = GameStateFactory(
            seed=41,
            visible_card_count=4,
            deck_card_count=16,
            total_bank_pebbles=100,
            card_pebble_count=5,
            num_equations=10,
            equation_lower_bound=1,
            equation_upper_bound=4,
            player_count=2,
        ).create()

        scoring = ScoringType.NORMAL

        referee = Referee(
            players=[
                PlayerMechanism(
                    "Alice",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
                PlayerMechanism(
                    "Bob",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
            ],
            scoring=scoring,
            game_state=game_state,
        )

        self.assertEqual((["Alice"], []), asyncio.run(referee.play()))

    def test_referee_initializes_with_default_game_state(self):
        referee = Referee(
            [
                PlayerMechanism(
                    "Alice",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
                PlayerMechanism(
                    "Bob",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
            ],
            scoring=ScoringType.NORMAL,

        )
        self.assertIsNotNone(referee.game_state)

        self.assertTrue(asyncio.run(referee.play()))

    def test_referee_returns_correct_winner(self):
        game_state = GameStateFactory(
            seed=41,
            visible_card_count=4,
            deck_card_count=160,
            total_bank_pebbles=100,
            card_pebble_count=5,
            num_equations=3,
            equation_lower_bound=1,
            equation_upper_bound=4,
            player_count=2,
        ).create()

        game_state.players[1].score = 19

        referee = Referee(
            players=[
                PlayerMechanism(
                    "Alice",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
                PlayerMechanism(
                    "Bob",
                    Strategy(
                        equation_search_depth=4,
                        value_function=lambda node: node.score,
                    ),
                ),
            ],
            scoring=ScoringType.NORMAL,
            game_state=game_state,
        )

        self.assertEqual((["Bob"], []), asyncio.run(referee.play()))


if __name__ == "__main__":
    unittest.main()
