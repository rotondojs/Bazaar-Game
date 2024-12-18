from copy import copy
from typing import TypeVar
from pydantic import BaseModel
from Bazaar.Common.equations import EquationTable, Equation
from Bazaar.Common.cards import Card
from Bazaar.Common.pebble_collection import PebbleCollection
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.transition_state import TransitionState

T = TypeVar("T")


class GameState(BaseModel):
    """The state of a game of Bazaar. Contains helper methods to advance the game state, based on taking individual
    in-game actions."""
    _equation_table: EquationTable
    _deck: list[Card]
    _tableau: list[Card]
    _bank: PebbleCollection
    _players: list[GamePlayer]
    _current_player_index: int
    _turn_section: TurnSection

    def __init__(
            self,
            equation_table: EquationTable,
            deck: list[Card],
            tableau: list[Card],
            bank: PebbleCollection,
            players: list[GamePlayer],
            current_player_index: int,
            turn_section: TurnSection,
    ) -> None:
        """
        Initialize a new GameState instance.

        Arguments:
            equation_table (EquationTable): The table of equations available for exchanges.
            deck (list[Card]): The deck of cards.
            tableau (list[Card]): The cards available for purchase.
            bank (PebbleCollection): The bank's pebble collection.
            players (list[GamePlayer]): The list of players in the game.
            current_player_index (int): The index of the current player.
            turn_section (TurnSection): The current "section" of the turn.
        """
        super().__init__()
        self._equation_table = equation_table
        self._deck = deck
        self._tableau = tableau
        self._bank = bank
        self._players = players
        self._current_player_index = current_player_index
        self._turn_section = turn_section

    def get_current_player(self) -> GamePlayer:
        """
        Get the current player.

        Returns:
            GamePlayer: The current player object.

        INVARIANT: The only way to change the current player is to call end_turn()
        which calls _move_to_next_player() which ensures that the current player
        is always active and that the index is always valid while the game is not over
        """
        return self._players[self._current_player_index]

    def get_repr_for_current_player(self) -> TurnState:
        """
        Get a representation of the game state for the current player.

        Returns:
            TurnState: A TurnState object containing the visible game state for the current player.
        """
        scores = [self._players[self._current_player_index].score]

        player_index = self._current_player_index

        for index in range(len(self._players) - 1):
            current_index = (player_index + index + 1) % len(self._players)

            if self._players[current_index].active:
                scores.append(self._players[current_index].score)

        return TurnState(
            tableau=copy(self._tableau),
            bank=copy(self._bank),
            scores=scores,
            player=self._players[self._current_player_index]
        )

    def apply_transition(self, state: TransitionState) -> None:
        """
        Apply a transition to the game state.

        Arguments:
            state (TransitionState): The resulting state of the transition.
        """
        player = self.get_current_player()

        player.wallet = state.pebbles
        player.score = state.score

        self._bank = state.bank
        self._turn_section = state.turn_section

        self._update_tableau(state.tableau)

    def purchase_card(self, card_index: int):
        self._players[self._current_player_index].purchase_card(self.tableau[card_index])

    def end_turn(self) -> None:
        """
        End the current player's turn and move to the next player.

        Raises:
            BazaarException: If the game is already over.
        """
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

        while not self.players[self._current_player_index].active:
            self._current_player_index = (self._current_player_index + 1) % len(self._players)

        self._turn_section = TurnSection.START_OF_TURN

    def kick_player(self, player_index: int) -> None:
        """
        Remove a player from the game.

        Arguments:
            player_index (int): The index of the player to kick.

        Raises:
            BazaarException: If there is no player with the given index.
        """

        try:
            self._players[player_index].active = False
        except IndexError:
            raise BazaarException(f"No player with index {player_index}")

        if self._current_player_index == player_index and any([p.active for p in self.players]):
            return self.end_turn()

    def burn_cards_from_deck(self, num_cards: int) -> None:
        """
        Burn a number of cards from the deck.

        Arguments:
            num_cards (int): The number of cards to burn.
        """
        if num_cards <= 0:
            return

        for _ in range(num_cards):
            if self._deck:
                self._deck.pop()
            else:
                self._tableau = []

    def _update_tableau(self, tableau: list[Card]) -> None:
        """
        Update the tableau by adding a new card from the deck if available.
        """
        diff = len(self._tableau) - len(tableau)

        if not diff:
            return

        self._tableau = tableau

        for _ in range(diff):
            if self._deck:
                self._tableau.append(self._deck.pop(0))

    @property
    def players(self):
        return self._players

    @property
    def list_of_equations(self) -> list[Equation]:
        return self._equation_table.get_equations()

    @property
    def tableau(self):
        return self._tableau

    @property
    def deck(self):
        return self._deck

    @property
    def bank(self):
        return self._bank

    @property
    def current_player_index(self):
        return self._current_player_index

    @property
    def turn_section(self):
        return self._turn_section
