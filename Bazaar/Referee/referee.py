import asyncio
from copy import copy, deepcopy
from typing import Optional, Callable

from pydantic import BaseModel, Field

from Bazaar.Common.equations import EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.pebble_collection import PebbleCollection
from Bazaar.Common.rule_book import RuleBook
from Bazaar.Common.scoring import ScoringType
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction
from Bazaar.Player.strategy import Strategy
from Bazaar.Referee.IObserver import IObserver
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.game_state_factory import GameStateFactory


class Referee(BaseModel):
    """
    The Referee class manages the game flow, player interactions, and rule enforcement for the Bazaar game.

    It acts as a proxy between all the players and the GameState, validating the moves through the RuleBook.

    Failure Modes Handled:
    - Invalid type of move: Ensures that all player actions are of the correct type.
    - Invalid move: Validates player moves against the rule book and handles invalid actions appropriately.
    - Exceptions: Kicks the player if any of the methods throw an exception instead of returning the expected value.

    INVARIANT: The number of elements in the 'players' list is always equal to the number of players in the game state.
               None of the arrays are modified so this invariant holds true throughout the lifetime of the Referee.
    """
    players: list[PlayerMechanism]
    scoring: ScoringType
    game_state: Optional[GameState] = None
    rule_book: RuleBook = Field(default_factory=RuleBook)
    observers: list[IObserver] = Field(default_factory=list)
    misbehaved: list[str] = Field(default_factory=list)
    draw_pebble: Callable[[PebbleCollection], PebbleCollection] = None
    player_timeout: Optional[int] = None

    def __init__(
            self,
            players,
            scoring,
            game_state=None,
            draw_pebble=None,
    ):
        """
        Initialize the Referee.

        Arguments:
            players (list[PlayerMechanism]): List of player mechanisms.
            game_state (Optional[GameState]): Initial game state. If None, a new game state is created.
        """
        super().__init__(players=players, scoring=scoring, game_state=game_state)

        if players is None:
            self.players = []

        if game_state is None:
            self.game_state = GameStateFactory(player_count=len(players)).create()

        if len(self.game_state.players) != len(players):
            raise ValueError("Number of players must match the game state.")

        if draw_pebble:
            self.draw_pebble = draw_pebble
        else:
            self.draw_pebble = RuleBook.draw_pebble

        self.player_timeout = 1

    async def play(self) -> tuple[list[str], list[str]]:
        """
        Play the game until completion.

        Returns:
            tuple[list[str], list[str]]: A tuple containing the list of winners' names and the list of misbehaved
             players' names.
        """
        await self._setup_game()

        while not self._check_game_over():
            await self.notify_observers()

            await self._request_pebble_or_trades()
            if self._check_game_over():
                continue

            await self._request_cards()
            if self._check_game_over():
                continue

            self.game_state.end_turn()

        self.assign_bonus_points()
        await self._notify_game_over()
        return await self._get_winner_and_misbehaved()

    def subscribe(self, observer: IObserver):
        """
        Subscribes the given observer to the referee's game.
        """
        self.observers.append(observer)

    async def notify_observers(self):
        for observer in self.observers:
            try:
                await asyncio.wait_for(observer.receive_state(deepcopy(self.game_state)), self.player_timeout)
            except Exception:
                pass

    def assign_bonus_points(self) -> None:
        RuleBook.assign_bonus_points(self.game_state, self.scoring)

    async def _notify_game_over(self) -> None:
        """
        Notify all players about the game's end and their win/loss status.
        """
        winner_indices = self.rule_book.find_winners(
            deepcopy(self.game_state)
        )

        for i, player in enumerate(self.players):
            if self.game_state.players[i].active:
                try:
                    await asyncio.wait_for(player.win(i in winner_indices), self.player_timeout)
                except BazaarException or asyncio.TimeoutError:
                    await self._tracked_kick_player(i)

        for observer in self.observers:
            try:
                await asyncio.wait_for(observer.game_over(), self.player_timeout)
            except Exception:
                pass

    async def _get_winner_and_misbehaved(self) -> tuple[list[str], list[str]]:
        """
        Get the list of winners and misbehaved players.

        Returns:
        tuple[list[str], list[str]]: A tuple containing the list of winners' names and the list of misbehaved players'
        names.
        """
        winners = []

        winner_indices = self.rule_book.find_winners(
            deepcopy(self.game_state)
        )

        for i in winner_indices:
            try:
                name = await asyncio.wait_for(self.players[i].name(), 1)
                winners.append(name)
            except BazaarException or asyncio.TimeoutError:
                await self._tracked_kick_player(i)

        misbehaved = copy(self.misbehaved)

        return winners, misbehaved

    def _check_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.rule_book.check_game_over(self.game_state)

    async def _request_pebble_or_trades(self) -> None:
        """
        Request pebble or trades action from the current player and apply the action if valid.
        """
        turn_state = self.game_state.get_repr_for_current_player()
        player = self.players[self.game_state.current_player_index]

        try:
            actions = await asyncio.wait_for(player.request_pebble_or_trades(turn_state), self.player_timeout)
            self._execute_pebble_or_trades(actions, turn_state)
        except BazaarException or asyncio.TimeoutError:
            await self._tracked_kick_player(self.game_state.current_player_index)

    def _execute_pebble_or_trades(self, actions: list[PlayerAction], turn_state: TurnState):
        for action in actions:
            if RuleBook.check_game_over(self.game_state):
                break

            transition = RuleBook.attempt_get_pebble_or_exchange(turn_state,
                                                                 EquationTable(self.game_state.list_of_equations),
                                                                 action,
                                                                 self.game_state.turn_section,
                                                                 self.draw_pebble)
            self.game_state.burn_cards_from_deck(transition.burn_cards)
            if self._check_game_over():
                return
            self.game_state.apply_transition(transition)
        self.game_state._turn_section = TurnSection.PURCHASING_CARDS

    async def _request_cards(self) -> None:
        """
        Request card purchase action from the current player and apply the action if valid.
        """
        turn_state = self.game_state.get_repr_for_current_player()
        player = self.players[self.game_state.current_player_index]

        try:
            actions = await asyncio.wait_for(player.request_cards(turn_state), self.player_timeout)
            self._execute_purchase_card(actions, turn_state)
        except BazaarException or asyncio.TimeoutError:
            await self._tracked_kick_player(self.game_state.current_player_index)

    def _execute_purchase_card(self, actions: list[PlayerAction], turn_state: TurnState):
        for action in actions:
            if RuleBook.check_game_over(self.game_state):
                break

            transition = RuleBook.attempt_purchase_card(action, turn_state, self.game_state.turn_section)

            self.game_state.purchase_card(action.options.index)
            self.game_state.apply_transition(transition)

    async def _setup_game(self):
        """
        Set up the game by calling the setup method for each player.
        """
        for i, player in enumerate(self.players):
            try:
                await asyncio.wait_for(player.setup(EquationTable(self.game_state.list_of_equations)),
                                       self.player_timeout)

            except BazaarException or asyncio.TimeoutError as e:
                await self._tracked_kick_player(i)

    async def _tracked_kick_player(self, index: int) -> None:
        """
        Kick a player from the game and track them as misbehaved.

        Arguments:
            index (int): The index of the player to be kicked.
        """
        self.game_state.kick_player(index)

        player = self.players[index]
        try:
            name = await asyncio.wait_for(player.name(), self.player_timeout)
        except BazaarException or asyncio.TimeoutError:
            # TODO: What to do if they never provide a name
            return
        self.misbehaved.append(name)


if __name__ == "__main__":
    referee = Referee(
        players=[
            PlayerMechanism(
                "John",
                Strategy(
                    equation_search_depth=4, value_function=lambda node: node.score
                ),
            ),
            PlayerMechanism(
                "Rishi",
                Strategy(
                    equation_search_depth=4,
                    value_function=lambda node: node.score,
                ),
            ),
        ],
        scoring=ScoringType.NORMAL)

    print(asyncio.run(referee.play()))
