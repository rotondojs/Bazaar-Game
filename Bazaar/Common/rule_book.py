from copy import copy
from typing import ClassVar, TypeVar, Callable

from pydantic import BaseModel

from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.pebble_collection import PebbleCollection, Color
from Bazaar.Common.scoring import ScoringType
from Bazaar.Common.transition_state import TransitionState
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.player_action import ActionType, PlayerAction
from Bazaar.Referee.game_state import GameState

T = TypeVar("T")


class RuleBook(BaseModel):
    """
    A class that encapsulates the rules and logic for the Bazaar game.

    This class provides methods to check the validity of various game actions
    based on the current game state and rules.
    """

    WINNING_SCORE: ClassVar[int] = 20

    """Scoring Constants"""
    MIN_PEBBLES_FOR_HIGH_BONUS: ClassVar[int] = 3
    MIN_PEBBLES_FOR_MEDIUM_BONUS: ClassVar[int] = 2
    MIN_PEBBLES_FOR_LOW_BONUS: ClassVar[int] = 1

    SCORE_HIGH_FACE: ClassVar[int] = 2
    SCORE_HIGH_NON_FACE: ClassVar[int] = 1
    SCORE_MEDIUM_FACE: ClassVar[int] = 3
    SCORE_MEDIUM_NON_FACE: ClassVar[int] = 2
    SCORE_LOW_FACE: ClassVar[int] = 5
    SCORE_LOW_NON_FACE: ClassVar[int] = 3
    SCORE_ZERO_FACE: ClassVar[int] = 8
    SCORE_ZERO_NON_FACE: ClassVar[int] = 5

    @staticmethod
    def draw_pebble(bank: PebbleCollection) -> PebbleCollection:
        """
            Select a pebble from the bank deterministically.

            Arguments:
                bank (PebbleCollection): The current bank

            Returns:
                PebbleCollection: A singleton collection with the pebble to be drawn
            """

        for color in Color:
            if bank[color] > 0:
                return PebbleCollection({color: 1})

    @staticmethod
    def attempt_get_pebble_or_exchange(
            turn_state: TurnState,
            equation_table: EquationTable,
            action: PlayerAction,
            turn_section: TurnSection,
            draw_pebble: Callable[[PebbleCollection], PebbleCollection]
    ) -> TransitionState:
        """
        Check if the current player can exchange a pebble or use equations based on the provided actions.

        Arguments:
            turn_state: The current state of the turn.
            equation_table: The table of equations available for the player.
            action: player action to check.
            turn_section: the turn section of the game.
            draw_pebble: the function to use to determine what pebble should be drawn.

        Returns:
            TransitionState: The resulting state if the action is valid

        Throws:
            BazaarException: if the player cannot draw a pebble or use equations based on the provided actions.
        """

        if (turn_section == TurnSection.START_OF_TURN
                and action == PlayerAction(action_type=ActionType.GET_PEBBLE)
                and len(turn_state.bank.as_list_of_colors()) > 0):
            pebble = draw_pebble(turn_state.bank)
            return TransitionState(pebbles=turn_state.player.wallet + pebble,
                                   bank=turn_state.bank - pebble,
                                   score=turn_state.scores[0],
                                   tableau=turn_state.tableau,
                                   burn_cards=0,
                                   turn_section=TurnSection.PURCHASING_CARDS)

        elif RuleBook._can_use_equation(action, turn_section):
            return RuleBook._apply_equation(action, turn_state, equation_table, turn_section)
        else:
            raise BazaarException("Invalid action")

    @staticmethod
    def attempt_purchase_card(action: PlayerAction, turn_state: TurnState,
                              turn_section: TurnSection) -> TransitionState:
        if RuleBook._can_purchase_card(action, turn_section):
            return RuleBook._apply_purchase(action, turn_state)
        else:
            raise BazaarException("Out of order purchase")

    @staticmethod
    def _can_use_equation(action, turn_section):
        return ((turn_section == TurnSection.START_OF_TURN
                 or turn_section == TurnSection.MAKING_EXCHANGES)
                and action.action_type == ActionType.USE_EQUATION)

    @staticmethod
    def _can_purchase_card(action, turn_section):
        return ((turn_section == TurnSection.PURCHASING_CARDS
                 or turn_section == TurnSection.MAKING_EXCHANGES)
                and action.action_type == ActionType.PURCHASE_CARD)

    @staticmethod
    def check_game_over(game_state: "GameState") -> bool:
        """
        Check if the game ending conditions are met.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return (
                not RuleBook.active_players(game_state)
                or RuleBook.winning_scores(game_state)
                or not game_state.tableau
                or (
                        sum(game_state.bank.values()) == 0
                        and RuleBook._no_player_can_buy_card(game_state)
                )
        )

    @staticmethod
    def active_players(game_state: "GameState") -> bool:
        return any(p.active for p in game_state.players)

    @staticmethod
    def winning_scores(game_state: "GameState") -> bool:
        return any(p.active and p.score >= RuleBook.WINNING_SCORE for p in game_state.players)

    @staticmethod
    def find_winners(game_state: "GameState") -> list[int]:
        """
        Returns a list of indices of all the winners of the game.

        Arguments:
            game_state: The current state of the game.

        Returns:
            list[int]: List of indices of players who won the game.
        """
        scores = []

        winning_scores = []

        for index, player in enumerate(game_state.players):
            if player.active:
                scores.append(player.score)

        if not scores:
            return winning_scores
        else:
            for index, player in enumerate(game_state.players):
                if player.score == max(scores):
                    winning_scores.append(index)

        return winning_scores

    @staticmethod
    def _no_player_can_buy_card(game_state: "GameState") -> bool:
        """
        Check if no player can buy any card in the tableau.

        Returns:
            bool: True if no player can buy a card, False otherwise.
        """
        return not any(
            any(card.can_acquire(player.wallet) and player.active for card in game_state.tableau)
            for player in game_state.players
        )

    @staticmethod
    def _apply_equation(
            action: PlayerAction,
            turn_state: TurnState,
            equation_table: EquationTable,
            turn_section: TurnSection
    ) -> TransitionState:
        """
        Apply equation exchanges based on player actions.

        Arguments:
            action (PlayerAction): player action to attempt.
            turn_state (TurnState): The current state of the turn.
            equation_table (EquationTable): The table of equations available for the player.

        Returns:
            TransitionState: The resulting state after applying the equations.

        Raises:
            BazaarException: If an invalid action is encountered, if the exchange is invalid, or if the turn section is
            incorrect.
        """
        pebbles = copy(turn_state.player.wallet)
        bank = copy(turn_state.bank)

        equation = RuleBook._handled_get(action.options.index, equation_table.get_equations())

        pebbles_in, pebbles_out = RuleBook._get_exchange_pebbles(equation, action.options.right_to_left)

        if RuleBook._can_perform_exchange(pebbles, bank, pebbles_in, pebbles_out):
            pebbles -= pebbles_in
            bank += pebbles_in

            bank -= pebbles_out
            pebbles += pebbles_out

            return RuleBook.create_exchange_transition_state(pebbles, bank, turn_state.scores[0], turn_state.tableau,
                                                             turn_section)
        else:
            raise BazaarException("Invalid exchange")

    @staticmethod
    def create_exchange_transition_state(pebbles: PebbleCollection, bank: PebbleCollection, score: int,
                                         tableau: list[Card], turn_section: TurnSection) -> TransitionState:
        return TransitionState(
            pebbles=pebbles,
            bank=bank,
            score=score,
            tableau=tableau,
            burn_cards=turn_section == TurnSection.START_OF_TURN,
            turn_section=TurnSection.MAKING_EXCHANGES,
        )

    @staticmethod
    def _apply_purchase(action: PlayerAction, turn_state: TurnState) -> TransitionState:
        """
        Apply card purchases based on player actions.

        Arguments:
            action (PlayerAction): Player action to check.
            turn_state (TurnState): The current state of the turn.

        Returns:
            TransitionState: The resulting state after purchasing cards.

        Raises:
            BazaarException: If an invalid action is encountered or if the purchase is invalid.
        """
        wallet = copy(turn_state.player.wallet)
        bank = turn_state.bank
        tableau = turn_state.tableau
        score = turn_state.scores[0]

        if action.options is None or action.options.index is None:
            raise BazaarException(f"player request not initialised fully {action}")

        index: int = action.options.index
        card = RuleBook._handled_get(index, tableau)

        try:
            if tableau[index] is None:
                raise BazaarException("Card was already purchased")

            wallet -= card.cost
            bank += card.cost
            score += RuleBook._score_player_card_purchase(wallet, card)
            # noinspection PyTypeChecker
            tableau[index] = None
        except ValueError:
            raise BazaarException("Card too expensive")

        return RuleBook.create_purchase_transition_state(wallet, bank, score, tableau)

    @staticmethod
    def create_purchase_transition_state(wallet: PebbleCollection, bank: PebbleCollection, score: int,
                                         tableau: list[Card]) -> TransitionState:
        return TransitionState(
            pebbles=wallet,
            bank=bank,
            score=score,
            tableau=[card for card in tableau if card],
            burn_cards=0,
            turn_section=TurnSection.PURCHASING_CARDS
        )

    @staticmethod
    def _score_player_card_purchase(wallet: PebbleCollection, card: Card) -> int:
        """
        Calculate the score for a player's card purchase.

        Arguments:
            wallet (PebbleCollection): The wallet of the player who purchased the card.
            card (Card): The card that was purchased.

        Returns:
            int: The score for the card purchase.
        """

        remaining_pebbles = sum(wallet.values())

        if remaining_pebbles >= RuleBook.MIN_PEBBLES_FOR_HIGH_BONUS:
            return RuleBook.SCORE_HIGH_FACE if card.face else RuleBook.SCORE_HIGH_NON_FACE

        elif remaining_pebbles >= RuleBook.MIN_PEBBLES_FOR_MEDIUM_BONUS:
            return RuleBook.SCORE_MEDIUM_FACE if card.face else RuleBook.SCORE_MEDIUM_NON_FACE

        elif remaining_pebbles >= RuleBook.MIN_PEBBLES_FOR_LOW_BONUS:
            return RuleBook.SCORE_LOW_FACE if card.face else RuleBook.SCORE_LOW_NON_FACE

        else:
            return RuleBook.SCORE_ZERO_FACE if card.face else RuleBook.SCORE_ZERO_NON_FACE

    @staticmethod
    def assign_bonus_points(state: GameState, scoring: ScoringType) -> None:
        """
        assign bonus points to the game state according to the scoring rules
        """
        for player in state.players:
            match scoring:
                case ScoringType.NORMAL:
                    pass
                case ScoringType.RWB:
                    rwb = PebbleCollection({Color.RED: 1, Color.WHITE: 1, Color.BLUE: 1})
                    if RuleBook._player_has_purchased(player, rwb):
                        player.score += 10
                case ScoringType.SEY:
                    sey = PebbleCollection({Color.RED: 1, Color.WHITE: 1, Color.BLUE: 1, Color.GREEN: 1,
                                            Color.YELLOW: 1})
                    if RuleBook._player_has_purchased(player, sey):
                        player.score += 50

    @staticmethod
    def _player_has_purchased(player: GamePlayer, req_pebbles: PebbleCollection) -> bool:
        """
        returns true if the player has purchased at least all the pebble in req_pebbles
        Args:
            player: the player to check
            req_pebbles: the pebbles the player must have purchased

        Returns:
            bool
        """
        total_purchase = PebbleCollection({})
        for card in player.purchased_cards:
            total_purchase += card.cost
        return total_purchase >= req_pebbles

    @staticmethod
    def _is_exchange_section(turn_section: TurnSection) -> bool:
        """
        Check if a player can use an equation in the current turn section.

        Arguments:
            turn_section (TurnSection): The current section of the turn.

        Returns:
            bool: True if the player can use an equation, False otherwise.
        """
        return turn_section in [
            TurnSection.START_OF_TURN,
            TurnSection.MAKING_EXCHANGES,
        ]

    @staticmethod
    def _can_perform_exchange(
            wallet: PebbleCollection,
            bank: PebbleCollection,
            pebbles_in: PebbleCollection,
            pebbles_out: PebbleCollection,
    ) -> bool:
        """
        Check if an exchange can be performed based on player and bank pebbles.

        Arguments:
            wallet (PebbleCollection): The wallet of the current player.
            bank (PebbleCollection): The bank's pebble collection.
            pebbles_in (PebbleCollection): Pebbles to be given by the player.
            pebbles_out (PebbleCollection): Pebbles to be received by the player.

        Returns:
            bool: True if the exchange can be performed, False otherwise.
        """
        return wallet >= pebbles_in and bank >= pebbles_out

    @staticmethod
    def _get_exchange_pebbles(
            equation: Equation, right_to_left: bool
    ) -> tuple[PebbleCollection, PebbleCollection]:
        """
        Get the input and output pebbles for an equation exchange.

        Arguments:
            equation (Equation): The equation to be used for the exchange.
            right_to_left (bool): True if the equation should be applied right to left, False otherwise.

        Returns:
            tuple[PebbleCollection, PebbleCollection]: A tuple containing the input and output pebble collections.
        """
        return (
            (equation.right, equation.left)
            if right_to_left
            else (equation.left, equation.right)
        )

    @staticmethod
    def _handled_get(index: int, collection: list[T]) -> T:
        """
        Safely get an item from a collection by index.

        Arguments:
            index (int): The index of the item to retrieve.
            collection (list[T]): The collection to retrieve the item from.

        Returns:
            T: The item at the specified index.

        Raises:
            BazaarException: If the index is out of range for the collection.
        """
        try:
            return collection[index]
        except IndexError:
            raise BazaarException(f"No {type(T)} with index {index}")
