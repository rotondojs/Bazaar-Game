import asyncio

from Bazaar.Common.equations import EquationTable
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction


class ExceptSetupPlayer(PlayerMechanism):
    # @override added in 3.12
    async def setup(self, equation_table: EquationTable) -> None:
        raise BazaarException()


class ExceptPorTPlayer(PlayerMechanism):
    # @override added in 3.12
    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        raise BazaarException()


class ExceptCardsPlayer(PlayerMechanism):
    # @override added in 3.12
    async def request_cards(self, turn_state: TurnState) -> list[PlayerAction]:
        raise BazaarException()


class ExceptWinPlayer(PlayerMechanism):
    # @override added in 3.12
    async def win(self, w: bool) -> None:
        raise BazaarException()
