from Bazaar.Common.equations import EquationTable
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction
from Bazaar.Player.strategy import Strategy


class _TimeoutPlayer(PlayerMechanism):
    timer: int = 1
    count: int = 0
    player: PlayerMechanism = None

    def __init__(self, name: str, strategy: Strategy, count: int):
        super().__init__(name, strategy)
        self.count = count
        self.player = PlayerMechanism(name, strategy)


class TimeoutSetupPlayer(_TimeoutPlayer):
    # @override added in 3.12
    async def setup(self, equation_table: EquationTable) -> None:
        if self.timer < self.count:
            self.timer += 1
            await self.player.setup(equation_table)
        else:
            while True:
                pass


class TimeoutPorTPlayer(_TimeoutPlayer):
    # @override added in 3.12
    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        if self.timer < self.count:
            self.timer += 1
            return await self.player.request_pebble_or_trades(turn_state)
        else:
            while True:
                pass


class TimeoutCardsPlayer(_TimeoutPlayer):
    # @override added in 3.12
    async def request_cards(self, turn_state: TurnState) -> list[PlayerAction]:
        if self.timer < self.count:
            self.timer += 1
            return await self.player.request_cards(turn_state)
        else:
            while True:
                pass


class TimeoutWinPlayer(_TimeoutPlayer):
    # @override added in 3.12
    async def win(self, w: bool) -> None:
        if self.timer < self.count:
            self.timer += 1
            await self.player.win(w)
        else:
            while True:
                pass
