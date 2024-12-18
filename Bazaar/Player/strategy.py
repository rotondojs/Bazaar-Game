import itertools
from copy import copy
from typing import Any, Callable
from pydantic import BaseModel, Field, NonNegativeInt

from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.pebble_collection import PebbleCollection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.player_action import ActionType, PlayerAction


class StrategyNode(BaseModel):
    """
    Represents a node in the strategy tree for the Bazaar game.

    This class encapsulates a subset of the turn state at a particular point in the game
    and the steps taken to reach that state.

    Attributes:
        pebbles (PebbleCollection): The player's current pebble collection.
        bank (PebbleCollection): The bank's current pebble collection.
        score (int): The player's current score.
        actions (list[PlayerAction]): The sequence of actions taken to reach this state.
        children (list[StrategyNode]): Child nodes representing possible future states.
    """

    pebbles: PebbleCollection
    bank: PebbleCollection
    score: int
    actions: list[PlayerAction] = Field(default_factory=list)
    children: list["StrategyNode"] = Field(default_factory=list)

    def __repr__(self) -> str:
        return self._repr_indented()

    def __hash__(self) -> int:
        return hash(
            (tuple(self.pebbles.values()),
             tuple(self.bank.values()),
             self.score,
             tuple(self.actions)))

    def __lt__(self, other: "StrategyNode") -> bool:
        if self.score != other.score:
            return self.score < other.score

        self_total_pebbles = sum(self.pebbles.values())
        other_total_pebbles = sum(other.pebbles.values())
        if self_total_pebbles != other_total_pebbles:
            return self_total_pebbles < other_total_pebbles

        return str(self.pebbles) < str(other.pebbles)

    def _repr_indented(self, depth: int = 0) -> str:
        indent = "  " * depth
        node_repr = f"{indent}StrategyNode(\n"
        node_repr += f"{indent}  pebbles={self.pebbles}, \n"
        node_repr += f"{indent}  bank={self.bank}, \n"
        node_repr += f"{indent}  score={self.score}, \n"
        node_repr += f"{indent}  actions={self.actions}, \n"
        node_repr += f"{indent}  children=[\n"

        if self.children:
            for child in self.children:
                node_repr += child._repr_indented(depth + 2) + ",\n"

        node_repr += f"{indent}] \n"
        node_repr += f"{indent})"
        return node_repr


class Strategy(BaseModel):
    """
    A class representing a strategy for playing the Bazaar game.

    This strategy uses a tree-based approach to evaluate possible moves and select the best one.
    It considers both equation exchanges and card purchases to maximize the player's score.

    Attributes:
        equation_search_depth (NonNegativeInt): The maximum depth to search for equation exchanges.
        value_function (Callable[[StrategyNode], int]): A function to evaluate the *value* of a strategy node.
    """

    equation_search_depth: NonNegativeInt
    value_function: Callable[[StrategyNode], int]

    def __init__(self, equation_search_depth: NonNegativeInt, value_function: Callable[[StrategyNode], int]):
        super().__init__(equation_search_depth=equation_search_depth, value_function=value_function)

    def request_pebble_or_trades(
            self, state: TurnState, equation_table: EquationTable
    ) -> list[PlayerAction]:
        """
        Determines whether to request a pebble or perform trades based on the current game state.

        Arguments:
            state (TurnState): The current state of the game.
            equation_table (EquationTable): the equation table of the game.

        Returns:
            list[PlayerAction]: A list of actions (either trades or a pebble request).
        """
        root = self._create_root_node(state)

        # TODO: error with using equations here prob with get usable
        if self._can_make_exchange(equation_table, state.player.wallet):
            actions = self._make_exchange_move(
                root, state, equation_table
            )

            if not actions:
                return [PlayerAction(ActionType.GET_PEBBLE)]

            out = list(filter(lambda move: move.action_type == ActionType.USE_EQUATION, actions))
            return out
        else:
            return [PlayerAction(ActionType.GET_PEBBLE)]

    def request_cards(self, state: TurnState) -> list[PlayerAction]:
        """
        Determines which cards to purchase based on the current game state.

        Arguments:
            state (TurnState): The current state of the game.

        Returns:
            list[PlayerAction]: A list of actions (card purchases).
        """
        root = self._create_root_node(state)

        return list(
            filter(
                lambda move: move.action_type == ActionType.PURCHASE_CARD,
                self._make_purchase_move(root, state),
            )
        )

    def _create_root_node(self, state: TurnState) -> StrategyNode:
        return self._create_node(state.player.wallet, state.bank, state.scores[0])

    def _make_exchange_move(
            self,
            root: StrategyNode,
            state: TurnState,
            equation_table: EquationTable
    ) -> list[PlayerAction]:

        self._add_exchange_neighbors(
            root,
            state.bank,
            equation_table,
            state.tableau,
            self.equation_search_depth,
        )

        candidates = self._find_best_candidates(root, self.value_function)
        best_candidate = self._break_ties_for_exchange_and_purchase(candidates, state.tableau, equation_table)
        return best_candidate.actions

    def _make_purchase_move(
            self, root: StrategyNode, state: TurnState
    ) -> list[PlayerAction]:
        self._add_card_purchases_to_node(root, state.tableau)

        candidates = self._find_best_candidates(root, self.value_function)
        best_candidates = self._break_ties_for_card_purchase(candidates, state.tableau)

        if len(best_candidates) == 1:
            best_candidate = best_candidates.pop()
        else:
            raise BazaarException("filtering failed to return unique purchase")
        return best_candidate.actions

    def _find_best_candidates(
            self, node: StrategyNode, value_function: Callable[[StrategyNode], int]
    ) -> set[StrategyNode]:
        all_candidates = self._flatten_tree(node)

        max_value = max(value_function(candidate) for candidate in all_candidates)
        return set(c for c in all_candidates if value_function(c) == max_value)

    def _flatten_tree(self, node: StrategyNode) -> list[StrategyNode]:
        return [node] + [
            child for child in node.children for child in self._flatten_tree(child)
        ]

    def _add_card_purchases_to_node(
            self, node: StrategyNode, tableau: list[Card]
    ) -> None:
        purchasable_cards = self._get_purchasable_cards(node.pebbles, tableau)
        permutations = itertools.permutations(purchasable_cards)

        for permutation in permutations:
            self._create_child_node_for_card_purchase(node, permutation)

    def _break_ties_for_exchange_and_purchase(
            self,
            candidates: set[StrategyNode],
            tableau: list[Card],
            equation_table: EquationTable
    ) -> StrategyNode:
        candidates = self._filter_for_smallest_exchange_sequence(
            self._break_ties_for_card_purchase(
                self._filter_minimum_trades(candidates), tableau
            ),
            equation_table
        )

        #if len(candidates) != 1:
            #raise BazaarException("filtering failed to return unique exchange")
        return candidates.pop()

    def _break_ties_for_card_purchase(
            self, candidates: set[StrategyNode], tableau: list[Card]
    ) -> set[StrategyNode]:
        candidates = self._filter_for_smallest_card_sequence(
            self._filter_for_smallest_wallet(
                self._filter_for_max_pebbles_in_wallet(
                    self._filter_for_max_points(candidates)
                )
            ),
            tableau,
        )

        return candidates

    @staticmethod
    def _filter_for_max_pebbles_in_wallet(
            candidates: set[StrategyNode]
    ) -> set[StrategyNode]:
        max_pebbles = max(sum(candidate.pebbles.values()) for candidate in candidates)
        return set(
            [
                candidate
                for candidate in candidates
                if sum(candidate.pebbles.values()) == max_pebbles
            ]
        )

    @staticmethod
    def _filter_for_max_points(
            candidates: set[StrategyNode]
    ) -> set[StrategyNode]:
        max_points = max(candidate.score for candidate in candidates)
        return set(
            [candidate for candidate in candidates if candidate.score == max_points]
        )

    def _filter_for_smallest_wallet(
            self, candidates: set[StrategyNode]
    ) -> set[StrategyNode]:
        if not candidates:
            return set()

        min_wallet_node = list(candidates)[0]
        best_candidates = [min_wallet_node]

        for candidate in candidates:
            if self._wallet_less_than(candidate.pebbles, min_wallet_node.pebbles):
                min_wallet_node = candidate
                best_candidates = [candidate]
            elif not self._wallet_less_than(min_wallet_node.pebbles, candidate.pebbles):
                best_candidates.append(candidate)

        return set(best_candidates)

    @staticmethod
    def _filter_sequence(
            candidates: set[StrategyNode],
            sequence_extractor: Callable[[StrategyNode], list],
            sequence_comparator: Callable[[list, list], bool],
    ) -> set[StrategyNode]:
        if not candidates:
            return set()

        min_sequence_node = list(candidates)[0]
        best_candidates = [min_sequence_node]

        for candidate in candidates:
            sequence1 = sequence_extractor(candidate)
            sequence2 = sequence_extractor(min_sequence_node)
            if sequence_comparator(sequence1, sequence2):
                min_sequence_node = candidate
                best_candidates = [candidate]
            elif not sequence_comparator(sequence2, sequence1):
                best_candidates.append(candidate)

        return set(best_candidates)

    def _filter_for_smallest_exchange_sequence(
            self, candidates: set[StrategyNode], equation_table: EquationTable
    ) -> set[StrategyNode]:
        return self._filter_sequence(
            candidates,
            lambda node: self._player_actions_to_exchange_sequence(
                node.actions, equation_table
            ),
            self._equation_sequence_less_than,
        )

    def _filter_for_smallest_card_sequence(
            self, candidates: set[StrategyNode], tableau: list[Card]
    ) -> set[StrategyNode]:
        return self._filter_sequence(
            candidates,
            lambda node: self._player_actions_to_card_sequence(node.actions, tableau),
            self._card_sequence_less_than,
        )

    @staticmethod
    def _player_actions_to_card_sequence(
            actions: list[PlayerAction], tableau: list[Card]
    ) -> list[Card]:

        card_purchases = filter(lambda _: _.action_type == ActionType.PURCHASE_CARD, actions)
        return [tableau[a.options.index] for a in card_purchases]

    @staticmethod
    def _player_actions_to_exchange_sequence(
            actions: list[PlayerAction], equation_table: EquationTable
    ) -> list[Equation]:

        exchange_actions = filter(lambda _: _.action_type == ActionType.USE_EQUATION, actions)
        equations = equation_table.get_equations()
        return [equations[a.options.index] for a in exchange_actions]

    def _card_less_than(self, card1: Card, card2: Card) -> bool:
        if card1.face != card2.face:
            return card1.face
        else:
            return self._wallet_less_than(card1.cost, card2.cost)

    @staticmethod
    def _sequence_less_than(
            sequence1: list,
            sequence2: list,
            element_comparator: Callable[[Any, Any], bool],
    ) -> bool:
        if len(sequence1) != len(sequence2):
            return len(sequence1) < len(sequence2)
        for elem1, elem2 in zip(sequence1, sequence2):
            if not element_comparator(elem1, elem2) and not element_comparator(
                    elem2, elem1
            ):
                continue
            return element_comparator(elem1, elem2)
        return False

    def _equation_sequence_less_than(
            self, sequence1: list[Equation], sequence2: list[Equation]
    ) -> bool:
        return self._sequence_less_than(sequence1, sequence2, self._equation_less_than)

    def _card_sequence_less_than(
            self, sequence1: list[Card], sequence2: list[Card]
    ) -> bool:
        # Prioritize sequences with lower indices
        if len(sequence1) != len(sequence2):
            return len(sequence1) < len(sequence2)
        for card1, card2 in zip(sequence1, sequence2):
            if card1 != card2:
                return self._card_less_than(card1, card2)
        return [card for card in sequence1] < [card for card in sequence2]

        #return self._sequence_less_than(sequence1, sequence2, self._card_less_than)

    def _equation_less_than(self, equation1: Equation, equation2: Equation) -> bool:
        if not self._wallet_less_than(
                equation1.left, equation2.left
        ) and not self._wallet_less_than(equation2.left, equation2.left):
            return self._wallet_less_than(equation1.right, equation2.right)

        return self._wallet_less_than(equation1.left, equation2.left)

    @staticmethod
    def _use_equation_count(node: StrategyNode) -> int:
        return sum(action.action_type == ActionType.USE_EQUATION for action in node.actions)

    def _filter_minimum_trades(
            self, candidates: set[StrategyNode]
    ) -> set[StrategyNode]:
        min_trades = min(
            self._use_equation_count(candidate) for candidate in candidates
        )
        return set(
            [
                candidate
                for candidate in candidates
                if self._use_equation_count(candidate) == min_trades
            ]
        )

    def _wallet_less_than(
            self, wallet1: PebbleCollection, wallet2: PebbleCollection
    ) -> bool:
        if self._wallet_size(wallet1) == self._wallet_size(wallet2):
            return self._wallet_to_string(wallet1) < self._wallet_to_string(wallet2)
        return self._wallet_size(wallet1) < self._wallet_size(wallet2)

    @staticmethod
    def _wallet_to_string(wallet: PebbleCollection) -> str:
        color_list = [color for color, count in wallet.items() for _ in range(count)]
        first_letters = [str(color)[0] for color in color_list]
        return "".join(sorted(first_letters))

    @staticmethod
    def _wallet_size(wallet: PebbleCollection) -> int:
        return sum(wallet.values())

    def _add_exchange_neighbors(
            self,
            node: StrategyNode,
            bank: PebbleCollection,
            equation_table: EquationTable,
            tableau: list[Card],
            max_depth: int
    ) -> StrategyNode:
        self._add_card_purchases_to_node(node, tableau)

        if max_depth == 0:
            return node

        for index, equation in enumerate(equation_table.get_equations()):
            for right_to_left in [False, True]:
                if equation.is_usable_in_direction(node.pebbles, bank, right_to_left):
                    child = self._create_child_node_for_equation(
                        node, equation, index, right_to_left
                    )
                    node.children.append(
                        self._add_exchange_neighbors(
                            child,
                            child.bank,
                            equation_table,
                            tableau,
                            max_depth - 1,
                        )
                    )

        return node

    @staticmethod
    def _get_purchasable_cards(
            pebbles: PebbleCollection, tableau: list[Card]
    ) -> list[tuple[int, Card]]:
        return [
            (i, card) for i, card in enumerate(tableau) if card.can_acquire(pebbles)
        ]

    def _create_child_node_for_card_purchase(
            self, parent: StrategyNode, remaining_purchases: tuple[tuple[int, Card]]
    ) -> None:
        if not remaining_purchases:
            return

        index, card = remaining_purchases[0]
        if card.can_acquire(parent.pebbles):
            new_pebbles, new_bank = self._apply_card_purchase(
                parent.pebbles, parent.bank, card
            )
            new_score = parent.score + self._score_card_purchase(card, new_pebbles)
            action = PlayerAction(ActionType.PURCHASE_CARD, index=index)

            child = StrategyNode(
                pebbles=new_pebbles,
                bank=new_bank,
                score=new_score,
                actions=parent.actions + [action],
            )

            parent.children.append(child)
            self._create_child_node_for_card_purchase(child, remaining_purchases[1:])

    @staticmethod
    def _apply_card_purchase(
            pebbles: PebbleCollection, bank: PebbleCollection, card: Card
    ) -> tuple[PebbleCollection, PebbleCollection]:
        new_pebbles = pebbles.model_copy(deep=True)
        new_bank = bank.model_copy(deep=True)

        new_pebbles -= card.cost
        new_bank += card.cost

        return new_pebbles, new_bank

    @staticmethod
    def _score_card_purchase(
            card: Card, remaining_pebbles: PebbleCollection
    ) -> int:
        total_pebbles = sum(remaining_pebbles.values())

        if total_pebbles >= 3:
            return 2 if card.face else 1
        elif total_pebbles >= 2:
            return 3 if card.face else 2
        elif total_pebbles >= 1:
            return 5 if card.face else 3
        else:
            return 8 if card.face else 5

    @staticmethod
    def _can_make_exchange(
            equation_table: EquationTable, pebbles: PebbleCollection
    ) -> bool:
        return len(equation_table.get_usable(pebbles)) > 0

    @staticmethod
    def _create_node(
            pebbles: PebbleCollection, bank: PebbleCollection, score: int
    ) -> StrategyNode:
        return StrategyNode(
            pebbles=copy(pebbles),
            bank=copy(bank),
            score=score,
        )

    def _create_child_node_for_equation(
            self, parent: StrategyNode, equation: Equation, index: int, right_to_left: bool
    ) -> StrategyNode:
        new_pebbles, new_bank = self._apply_equation(
            parent.pebbles, parent.bank, equation, right_to_left
        )

        action = PlayerAction(
            ActionType.USE_EQUATION,
            index=index,
            right_to_left=right_to_left,
        )

        return StrategyNode(
            pebbles=new_pebbles,
            bank=new_bank,
            score=parent.score,
            actions=parent.actions + [action],
        )

    @staticmethod
    def _apply_equation(
            pebbles: PebbleCollection,
            bank: PebbleCollection,
            equation: Equation,
            right_to_left: bool,
    ) -> tuple[PebbleCollection, PebbleCollection]:
        new_pebbles = pebbles.model_copy(deep=True)
        new_bank = bank.model_copy(deep=True)

        subtract_from_pebbles = equation.right if right_to_left else equation.left
        add_to_pebbles = equation.left if right_to_left else equation.right

        new_pebbles -= subtract_from_pebbles
        new_pebbles += add_to_pebbles

        new_bank += subtract_from_pebbles
        new_bank -= add_to_pebbles

        return new_pebbles, new_bank


if __name__ == "__main__":
    max_score: Callable[[StrategyNode], int] = lambda node: node.score

    max_cards: Callable[[StrategyNode], int] = lambda node: [
        1 for action in node.actions if action.action_type == ActionType.PURCHASE_CARD
    ].count(1)
