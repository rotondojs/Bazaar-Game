from Bazaar.Common.equations import EquationTable
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction
from Bazaar.Player.strategy import Strategy


class InvalidMechanism(PlayerMechanism):
    def __init__(self) -> None:
        super().__init__(
            "",
            strategy=Strategy(
                equation_search_depth=4, value_function=lambda node: node.score
            ),
        )

    async def setup(self, equation_table: EquationTable) -> None: ...

    async def name(self) -> str:
        return "MOCK"

    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        return None  # noqa

    async def request_cards(self, turn_state: TurnState) -> list[PlayerAction]:
        return "cards"  # noqa

    async def win(self, w: bool) -> None: ...
