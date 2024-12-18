from Bazaar.Common.pebble_collection import Color
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction, ActionType


class CheatNonExistentEquation(PlayerMechanism):
    # @override added in 3.12
    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        return [PlayerAction(ActionType.USE_EQUATION, index=len(self.equation_table.get_equations()),
                             right_to_left=False)]


class CheatBankCannotTrade(PlayerMechanism):
    # @override added in 3.12
    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        for index, eq in enumerate(self.list_of_equations):
            if any(eq.left[color] > turn_state.bank[color] for color in Color):
                return [PlayerAction(ActionType.USE_EQUATION, index=index, right_to_left=True)]
            if any(eq.right[color] > turn_state.bank[color] for color in Color):
                return [PlayerAction(ActionType.USE_EQUATION, index=index, right_to_left=False)]
        return self.strategy.request_pebble_or_trades(turn_state, self.list_of_equations)


class CheatWalletCannotTrade(PlayerMechanism):
    # @override added in 3.12
    async def request_pebble_or_trades(self, state: TurnState) -> list[PlayerAction]:
        for index, eq in enumerate(self.list_of_equations):
            if any(eq.left[color] > state.wallet[color] for color in Color):
                return [PlayerAction(ActionType.USE_EQUATION, index=index, right_to_left=False)]
            if any(eq.right[color] > state.wallet[color] for color in Color):
                return [PlayerAction(ActionType.USE_EQUATION, index=index, right_to_left=True)]
        return self.strategy.request_pebble_or_trades(state, self.list_of_equations)


class CheatBuyUnavailableCard(PlayerMechanism):
    # @override added in 3.12
    async def request_cards(self, state: TurnState) -> list[PlayerAction]:
        return [PlayerAction(ActionType.PURCHASE_CARD, index=len(state.tableau))]


class CheatWalletCannotBuyCard(PlayerMechanism):
    # @override added in 3.12
    async def request_cards(self, state: TurnState) -> list[PlayerAction]:
        for index, card in enumerate(state.tableau):
            if not card.can_acquire(state.wallet):
                return [PlayerAction(ActionType.PURCHASE_CARD, index=len(state.tableau))]
        return self.strategy.request_cards(state)
