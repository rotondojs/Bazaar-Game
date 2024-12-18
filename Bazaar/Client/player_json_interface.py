import json

from Bazaar.Common.JSON.returns import Returns
from Bazaar.Common.JSON.serializer import BazaarSerializer
from Bazaar.Common.equations import EquationTable
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism


class PlayerJsonInterface:
    _player: PlayerMechanism
    _equations: EquationTable

    def __init__(self, player: PlayerMechanism):
        self._player = player

    async def setup(self, equations: EquationTable) -> json:
        self._equations = equations
        await self._player.setup(self._equations)
        return json.dumps(Returns.VOID)

    async def request_pebble_or_trades(self, state: TurnState) -> json:
        list_player_action = await self._player.request_pebble_or_trades(state)
        if len(list_player_action) != 0:
            equations = self._equations.equations
            output = EquationTable([equations[a.options.index] for a in list_player_action])
            return json.dumps(BazaarSerializer.equations(output))
        else:
            return json.dumps(Returns.FALSE)

    async def request_cards(self, state: TurnState) -> json:
        list_player_action = await self._player.request_cards(state)
        tableau = state.tableau
        cards = [tableau[a.options.index] for a in list_player_action]
        return json.dumps(BazaarSerializer.cards(cards))

    async def win(self, won: str) -> json:
        await self._player.win(won != Returns.FALSE)
        return json.dumps(Returns.VOID)
