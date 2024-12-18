from pydantic import BaseModel, Field

from Bazaar.Common.equations import EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.player_action import PlayerAction
from Bazaar.Player.strategy import Strategy


class PlayerMechanism(BaseModel):
    """
    Represents a player mechanism in the Bazaar game.

    It provides methods for setting up the player, requesting actions, and handling game outcomes.
    """

    player_name: str
    strategy: Strategy
    equation_table: EquationTable = Field(default_factory=lambda: EquationTable([]))

    class Config:
        extra = "allow"

    def __init__(self, player_name: str, strategy: Strategy) -> None:
        """
        Initialize a PlayerMechanism instance.

        Arguments:
            player_name (str): The name of the player.
            strategy (Strategy): The strategy object used by the player.
        """
        super().__init__(player_name=player_name, strategy=strategy)

    async def setup(self, equation_table: EquationTable) -> None:
        """
        Set up the player's equation table.

        Arguments:
            equation_table (EquationTable): The equation table to be used by the player.
        """
        if not self.equation_table.equations:
            self.equation_table = equation_table
        else:
            raise BazaarException("Equation table can only be setup once")

    async def name(self) -> str:
        """
        Get the player's name.

        Returns:
            str: The name of the player.
        """
        return self.player_name

    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        """
        Request pebble or trade actions based on the current turn state.

        Arguments:
            turn_state (TurnState): The current state of the turn.

        Returns:
            list[PlayerAction]: A list of player actions for pebble or trade requests.
        """
        return self.strategy.request_pebble_or_trades(turn_state, self.equation_table)

    async def request_cards(self, turn_state: TurnState) -> list[PlayerAction]:
        """
        Request card actions based on the current turn state.

        Arguments:
            turn_state (TurnState): The current state of the turn.

        Returns:
            list[PlayerAction]: A list of player actions for card requests.
        """
        return self.strategy.request_cards(turn_state)

    async def win(self, w: bool) -> None:
        """
        Handle the game outcome for the player.

        Arguments:
            w (bool): True if the player won, False otherwise.
        """
        ...
