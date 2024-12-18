import unittest

from Bazaar.Common.JSON.deserializer import BazaarDeserializer
from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.pebble_collection import PebbleCollection, Color
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.player_action import ActionType, PlayerAction
from Bazaar.Player.strategy import Strategy, StrategyNode


class TestGameState(unittest.TestCase):
    table: EquationTable
    tableau: list[Card]
    bank: PebbleCollection
    player: GamePlayer
    strategy: Strategy

    def setUp(self):
        a = Equation(PebbleCollection({Color.WHITE: 1}),
                     PebbleCollection({Color.YELLOW: 1}))
        b = Equation(PebbleCollection({Color.BLUE: 2}),
                     PebbleCollection({Color.GREEN: 1}))
        c = Equation(PebbleCollection({Color.GREEN: 3}),
                     PebbleCollection({Color.RED: 1}))

        self.table = EquationTable([a,
                                    b,
                                    c])

        self.tableau = [
            Card(cost=PebbleCollection({Color.RED: 4, Color.BLUE: 1}), face=True),
            Card(cost=PebbleCollection({Color.BLUE: 3, Color.GREEN: 2}), face=False),
            Card(
                cost=PebbleCollection({Color.RED: 4, Color.GREEN: 1}),
                face=False,
            ),
        ]

        self.bank = PebbleCollection({Color.RED: 10, Color.BLUE: 10, Color.GREEN: 10})

        self.player = GamePlayer(
            pebbles=PebbleCollection({Color.RED: 4, Color.BLUE: 4, Color.GREEN: 2}),
            score=0,
            active=True,
            purchased_cards=[]
        )

        self.update_turn_state()

        self.strategy = Strategy(
            equation_search_depth=4, value_function=lambda n: n.score
        )

    def update_turn_state(self) -> None:
        self.turn_state = TurnState(
            self.tableau,
            self.bank,
            [0],
            self.player
        )

    def test_strategy_node_compare(self):
        self.table = EquationTable([
            Equation(left=PebbleCollection({Color.BLUE: 3, Color.GREEN: 1}),
                     right=PebbleCollection({Color.RED: 1, Color.YELLOW: 1})),
            Equation(left=PebbleCollection({Color.YELLOW: 1, Color.WHITE: 1}),
                     right=PebbleCollection({Color.GREEN: 1})),
            Equation(left=PebbleCollection({Color.BLUE: 1}),
                     right=PebbleCollection({Color.YELLOW: 4})),
            Equation(left=PebbleCollection({Color.WHITE: 3}),
                     right=PebbleCollection({Color.RED: 2, Color.BLUE: 2})),
            Equation(left=PebbleCollection({Color.YELLOW: 1, Color.RED: 3}),
                     right=PebbleCollection({Color.BLUE: 1, Color.WHITE: 1})),
            Equation(left=PebbleCollection({Color.GREEN: 1}),
                     right=PebbleCollection({Color.WHITE: 1, Color.BLUE: 3})),
            Equation(left=PebbleCollection({Color.RED: 3, Color.YELLOW: 1}),
                     right=PebbleCollection({Color.WHITE: 2})),
            Equation(left=PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1}),
                     right=PebbleCollection({Color.RED: 4})),
            Equation(left=PebbleCollection({Color.RED: 2}),
                     right=PebbleCollection({Color.BLUE: 1, Color.YELLOW: 1})),
            Equation(left=PebbleCollection({Color.WHITE: 2, Color.RED: 2}),
                     right=PebbleCollection({Color.BLUE: 1}))])

        self.turn_state = BazaarDeserializer._state_to_bazaar_game_state(
            {"bank": ["red", "red", "red", "red", "red", "red", "red", "red",
                      "red", "red", "red", "red", "red", "red", "red", "red",
                      "red", "red", "white", "white", "white", "white",
                      "white", "white", "white", "white", "white", "white",
                      "white", "white", "white", "white", "white", "white",
                      "white", "white", "white", "white", "white", "blue",
                      "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue",
                      "blue", "blue", "blue", "blue", "blue", "blue", "green", "green", "green", "green", "green",
                      "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "green",
                      "green", "green", "green", "green", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow",
                      "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow",
                      "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"],
             "visibles": [{"pebbles": ["red", "red", "blue", "blue", "green"], "face?": True},
                          {"pebbles": ["blue", "blue", "green", "yellow", "yellow"], "face?": True},
                          {"pebbles": ["red", "red", "blue", "blue", "green"], "face?": True},
                          {"pebbles": ["white", "green", "green", "yellow", "yellow"], "face?": False}],
             "cards": [],
             "players": [{"wallet": ["white", "blue"], "score": 2, "cards": []}]},
            self.table).get_repr_for_current_player()
        self.tableau = self.turn_state.tableau

        issue = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 1, Color.WHITE: 4}),
            bank=PebbleCollection({Color.RED: 19, Color.WHITE: 17, Color.BLUE: 19, Color.GREEN: 20, Color.YELLOW: 21}),
            score=2,
            actions=[PlayerAction(ActionType.USE_EQUATION, index=8, right_to_left=False),
                     PlayerAction(ActionType.USE_EQUATION, index=9, right_to_left=True),
                     PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                     PlayerAction(ActionType.USE_EQUATION, index=9, right_to_left=True),
                     PlayerAction(ActionType.PURCHASE_CARD, index=0)],
            children=[
            ]
        ), StrategyNode(
            pebbles=PebbleCollection({Color.RED: 1, Color.WHITE: 4}),
            bank=PebbleCollection({Color.RED: 19, Color.WHITE: 17, Color.BLUE: 19, Color.GREEN: 20, Color.YELLOW: 21}),
            score=2,
            actions=[PlayerAction(ActionType.USE_EQUATION, index=8, right_to_left=False),
                     PlayerAction(ActionType.USE_EQUATION, index=9, right_to_left=True),
                     PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                     PlayerAction(ActionType.USE_EQUATION, index=9, right_to_left=True),
                     PlayerAction(ActionType.PURCHASE_CARD, index=2)],
            children=[
            ]
        )}

        # PlayerAction(ActionType.PURCHASE_CARD, index=2, right_to_left=None)



        s = Strategy(
            equation_search_depth=4,
            value_function=lambda node: node.score,
        )
        #self.assertEqual(1, len(s._filter_for_smallest_wallet(issue)))
        #self.assertEqual(1, len(s._break_ties_for_card_purchase(issue, self.tableau)))
        # TODO: this line should not raise an exception
        #self.assertRaises(BazaarException, s._break_ties_for_exchange_and_purchase, issue, self.tableau, self.table)

        #self.assertFalse(True)

        filtered_candidates = s._break_ties_for_card_purchase(issue, self.tableau)
        print(f"Filtered Candidates: {filtered_candidates}")
        print(f"Number of Candidates: {len(filtered_candidates)}")

    def test_make_move_no_valid_equation_or_cards(self):
        self.table = EquationTable(
            [
                Equation(
                    PebbleCollection({Color.WHITE: 1}),
                    PebbleCollection({Color.YELLOW: 1}),
                )
            ]
        )

        self.tableau = []

        self.update_turn_state()

        self.assertEqual(
            self.strategy.request_pebble_or_trades(self.turn_state, self.table),
            [PlayerAction(ActionType.GET_PEBBLE)],
        )

    def test_make_move_no_valid_equation(self):
        self.table = EquationTable(
            [
                Equation(
                    PebbleCollection({Color.WHITE: 1}),
                    PebbleCollection({Color.YELLOW: 1}),
                )
            ]
        )

        self.update_turn_state()

        self.assertEqual(
            self.strategy.request_cards(self.turn_state),
            [
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
            ],
        )

    def test_make_move_no_valid_cards(self):
        self.tableau = []

        self.update_turn_state()

        self.assertEqual(
            self.strategy.request_cards(self.turn_state),
            [],
        )

    def test_make_move_cards_present(self):
        self.assertEqual(
            self.strategy.request_cards(self.turn_state),
            [
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
            ],
        )

    def test_make_move_must_use_equations(self):
        # print(self.player.pebbles)

        self.player.wallet -= PebbleCollection({Color.RED: 1, Color.BLUE: 1})

        self.update_turn_state()

        # print(self.strategy.request_pebble_or_trades(self.turn_state, self.table))

        self.assertEqual([
            PlayerAction(ActionType.USE_EQUATION, index=1, right_to_left=False),
            PlayerAction(ActionType.USE_EQUATION, index=2, right_to_left=False)
        ],
            self.strategy.request_pebble_or_trades(self.turn_state, self.table)
        )

    def test_filter_for_max_pebbles_in_wallet(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 1}),
            score=0,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=0,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 3}),
            score=0,
            bank=PebbleCollection({}),
        )}

        return self.assertEqual(
            self.strategy._filter_for_max_pebbles_in_wallet(candidates),
            {StrategyNode(
                pebbles=PebbleCollection({Color.GREEN: 3}),
                score=0,
                bank=PebbleCollection({}),
            )},
        )

    def test_filter_for_max_pebbles_in_wallet_multiple(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 1}),
            score=0,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=0,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 3}),
            score=0,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 3}),
            score=0,
            bank=PebbleCollection({}),
        )}

        return self.assertEqual(
            self.strategy._filter_for_max_pebbles_in_wallet(candidates),
            {StrategyNode(
                pebbles=PebbleCollection({Color.GREEN: 3}),
                score=0,
                bank=PebbleCollection({}),
            ), StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 3}),
                score=0,
                bank=PebbleCollection({}),
            )},
        )

    def test_filter_for_max_points(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
        )}

        return self.assertEqual(
            self.strategy._filter_for_max_points(candidates),
            {StrategyNode(
                pebbles=PebbleCollection({Color.GREEN: 2}),
                score=3,
                bank=PebbleCollection({}),
            )},
        )

    def test_filter_for_max_points_multiple(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 4}),
            score=3,
            bank=PebbleCollection({}),
        )}

        return self.assertEqual(
            self.strategy._filter_for_max_points(candidates),
            {StrategyNode(
                pebbles=PebbleCollection({Color.GREEN: 2}),
                score=3,
                bank=PebbleCollection({}),
            ), StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 4}),
                score=3,
                bank=PebbleCollection({}),
            )},
        )

    def test_filter_for_smallest_wallet(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
        )}

        return self.assertEqual(
            self.strategy._filter_for_smallest_wallet(candidates),
            {StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 2}),
                score=2,
                bank=PebbleCollection({}),
            )},
        )

    def test_filter_for_smallest_wallet_different_size(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 4}),
            score=3,
            bank=PebbleCollection({}),
        )}

        return self.assertEqual(
            self.strategy._filter_for_smallest_wallet(candidates),
            {StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 2}),
                score=2,
                bank=PebbleCollection({}),
            )},
        )

    def test_filter_for_smallest_card_sequence(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
                PlayerAction(ActionType.PURCHASE_CARD, index=2),
            ],
        )}

        return self.assertEqual(
            self.strategy._filter_for_smallest_card_sequence(candidates, self.tableau),
            {StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 2}),
                score=2,
                bank=PebbleCollection({}),
                actions=[
                    PlayerAction(ActionType.PURCHASE_CARD, index=0),
                ],
            )},
        )

    def test_filter_for_smallest_card_sequence_same_size(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.PURCHASE_CARD, index=0),
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
                PlayerAction(ActionType.PURCHASE_CARD, index=2),
            ],
        )}

        return self.assertEqual(
            self.strategy._filter_for_smallest_card_sequence(candidates, self.tableau),
            {StrategyNode(
                pebbles=PebbleCollection({Color.RED: 2}),
                score=1,
                bank=PebbleCollection({}),
                actions=[
                    PlayerAction(ActionType.PURCHASE_CARD, index=0),
                    PlayerAction(ActionType.PURCHASE_CARD, index=1),
                ],
            ), StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 2}),
                score=2,
                bank=PebbleCollection({}),
                actions=[
                    PlayerAction(ActionType.PURCHASE_CARD, index=0),
                    PlayerAction(ActionType.PURCHASE_CARD, index=1),
                ],
            )},
        )

    def test_filter_for_smallest_exchange_sequence_check_2(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=1, right_to_left=False
                ),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=3,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=1, right_to_left=False
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=2, right_to_left=True
                ),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=1, right_to_left=False
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=2, right_to_left=True
                ),
            ],
        )}

        return self.assertEqual(
            self.strategy._filter_for_smallest_exchange_sequence(
                candidates, self.table
            ),
            {StrategyNode(
                pebbles=PebbleCollection({Color.RED: 2}),
                score=1,
                bank=PebbleCollection({}),
                actions=[
                    PlayerAction(
                        action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                    ),
                    PlayerAction(
                        action_type=ActionType.USE_EQUATION, index=1, right_to_left=False
                    ),
                ],
            )},
        )

    def test_filter_for_smallest_exchange_sequence(self):
        candidates = {StrategyNode(
            pebbles=PebbleCollection({Color.RED: 2}),
            score=1,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=1, right_to_left=False
                ),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.BLUE: 2}),
            score=2,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                ),
            ],
        ), StrategyNode(
            pebbles=PebbleCollection({Color.GREEN: 2}),
            score=3,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=1, right_to_left=False
                ),
                PlayerAction(
                    action_type=ActionType.USE_EQUATION, index=2, right_to_left=True
                ),
            ],
        )}

        return self.assertEqual(
            self.strategy._filter_for_smallest_exchange_sequence(
                candidates, self.table
            ),
            {StrategyNode(
                pebbles=PebbleCollection({Color.BLUE: 2}),
                score=2,
                bank=PebbleCollection({}),
                actions=[
                    PlayerAction(
                        action_type=ActionType.USE_EQUATION, index=0, right_to_left=True
                    ),
                ],
            )},
        )

    def test_wallet_to_string_empty(self):
        return self.assertEqual(
            self.strategy._wallet_to_string(PebbleCollection({})), ""
        )

    def test_wallet_to_string_single(self):
        return self.assertEqual(
            self.strategy._wallet_to_string(PebbleCollection({Color.RED: 1})), "R"
        )

    def test_wallet_to_string_multiple(self):
        return self.assertEqual(
            self.strategy._wallet_to_string(
                PebbleCollection({Color.RED: 1, Color.BLUE: 2})
            ),
            "BBR",
        )

    def test_wallet_less_than_same_size(self):
        return self.assertTrue(
            self.strategy._wallet_less_than(
                PebbleCollection({Color.RED: 1, Color.BLUE: 2}),
                PebbleCollection({Color.RED: 1, Color.GREEN: 2}),
            )
        )

    def test_wallet_less_than_different_size(self):
        return self.assertTrue(
            self.strategy._wallet_less_than(
                PebbleCollection({Color.RED: 1, Color.BLUE: 2}),
                PebbleCollection({Color.RED: 1, Color.BLUE: 2, Color.GREEN: 2}),
            )
        )

    def test_wallet_less_than_same_size_2(self):
        return self.assertFalse(
            self.strategy._wallet_less_than(
                PebbleCollection({Color.RED: 1, Color.BLUE: 2}),
                PebbleCollection({Color.RED: 1, Color.BLUE: 2}),
            )
        )

    def test_wallet_size_empty(self):
        return self.assertEqual(self.strategy._wallet_size(PebbleCollection({})), 0)

    def test_wallet_size_single(self):
        return self.assertEqual(
            self.strategy._wallet_size(PebbleCollection({Color.RED: 1})), 1
        )

    def test_wallet_size_multiple(self):
        return self.assertEqual(
            self.strategy._wallet_size(PebbleCollection({Color.RED: 1, Color.BLUE: 2})),
            3,
        )

    def test_player_actions_to_card_sequence_empty(self):
        actions = []

        return self.assertEqual(
            self.strategy._player_actions_to_card_sequence(actions, self.tableau), []
        )

    def test_player_actions_to_card_sequence(self):
        actions = [
            PlayerAction(ActionType.PURCHASE_CARD, index=0),
            PlayerAction(ActionType.PURCHASE_CARD, index=1),
        ]

        return self.assertEqual(
            self.strategy._player_actions_to_card_sequence(actions, self.tableau),
            [self.tableau[0], self.tableau[1]],
        )

    def test_player_actions_to_card_sequence_no_cards(self):
        actions = [PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True)]

        return self.assertEqual(
            self.strategy._player_actions_to_card_sequence(actions, self.tableau), []
        )

    def test_player_actions_to_exchange_sequence_empty(self):
        actions = []

        return self.assertEqual(
            self.strategy._player_actions_to_exchange_sequence(actions, self.table), []
        )

    def test_player_actions_to_exchange_sequence(self):
        actions = [
            PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
            PlayerAction(ActionType.USE_EQUATION, index=1, right_to_left=False),
        ]

        equations = self.table.get_equations()

        return self.assertEqual(
            self.strategy._player_actions_to_exchange_sequence(actions, self.table),
            [equations[0], equations[1]],
        )

    def test_use_equation_count_empty(self):
        node = StrategyNode(
            pebbles=PebbleCollection({}), score=0, bank=PebbleCollection({})
        )

        return self.assertEqual(self.strategy._use_equation_count(node), 0)

    def test_use_equation_count_single(self):
        node = StrategyNode(
            pebbles=PebbleCollection({Color.RED: 1}),
            score=0,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(action_type=ActionType.USE_EQUATION, index=0, right_to_left=True)
            ],
        )

        return self.assertEqual(self.strategy._use_equation_count(node), 1)

    def test_use_equation_count_multiple(self):
        node = StrategyNode(
            pebbles=PebbleCollection({Color.RED: 1, Color.BLUE: 2}),
            score=0,
            bank=PebbleCollection({}),
            actions=[
                PlayerAction(ActionType.USE_EQUATION, index=0, right_to_left=True),
                PlayerAction(ActionType.USE_EQUATION, index=1, right_to_left=False),
                PlayerAction(ActionType.PURCHASE_CARD, index=1),
            ],
        )

        return self.assertEqual(self.strategy._use_equation_count(node), 2)

    def test_can_make_exchange_empty(self):
        return self.assertFalse(
            self.strategy._can_make_exchange(self.table, PebbleCollection({}))
        )

    def test_can_make_exchange_single(self):
        return self.assertTrue(
            self.strategy._can_make_exchange(
                self.table, PebbleCollection({Color.WHITE: 1})
            )
        )

    def test_can_make_exchange_multiple(self):
        return self.assertTrue(
            self.strategy._can_make_exchange(
                self.table, PebbleCollection({Color.WHITE: 1, Color.BLUE: 2})
            )
        )

    def test_get_purchasable_cards_empty(self):
        return self.assertEqual(
            self.strategy._get_purchasable_cards(PebbleCollection({}), self.tableau), []
        )

    def test_get_purchasable_cards_single(self):
        return self.assertEqual(
            self.strategy._get_purchasable_cards(
                PebbleCollection({Color.RED: 4, Color.BLUE: 1}), self.tableau
            ),
            [(0, self.tableau[0])],
        )


if __name__ == "__main__":
    unittest.main()
