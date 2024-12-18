import json
import socket

from Bazaar.Common.JSON.deserializer import BazaarDeserializer
from Bazaar.Common.JSON.returns import Returns
from Bazaar.Common.JSON.serializer import BazaarSerializer
from Bazaar.Common.equations import EquationTable, Equation
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.JSON.methods import Methods
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import PlayerAction, ActionType
from Bazaar.Player.strategy import Strategy


class ProxyPlayer(PlayerMechanism):
    equations: list[Equation]
    socket: socket = None

    def __init__(self, name, player_socket: socket):
        # TODO: dummy Strategy created and never used, should refactor strategy to be optional
        super().__init__(name, Strategy(0, lambda _: _))
        self.socket = player_socket

    async def setup(self, equation_table: EquationTable) -> None:
        """
        send the equation table to the remote player

        Arguments:
            equation_table (EquationTable): The equation table to be used by the player.
        """
        self.equations = equation_table.get_equations()
        self._send([Methods.SETUP.name, BazaarSerializer.equations(equation_table)])
        if self._receive() == "void":
            return
        else:
            raise BazaarException("The player was not setup")

    async def request_pebble_or_trades(self, turn_state: TurnState) -> list[PlayerAction]:
        """
        Request a pebble or trade actions from the remote player based on the current turn state.

        Arguments:
            turn_state (TurnState): The current state of the turn.

        Returns:
            list[PlayerAction]: A list of player actions for pebble or trade requests.
        """
        self._send([Methods.REQUEST_P_OR_T.name, BazaarSerializer.turn_state(turn_state)])
        response = self._receive()
        if not response:
            return [PlayerAction(action_type=ActionType.GET_PEBBLE)]
        else:
            rules = BazaarDeserializer.equations_to_equation_table(response).get_equations()
            output = []
            for rule in rules:
                try:
                    output.append(PlayerAction(ActionType.USE_EQUATION,
                                               index=self.equations.index(rule),
                                               right_to_left=False))
                except ValueError:
                    try:
                        output.append(PlayerAction(ActionType.USE_EQUATION,
                                                   index=self.equations.index(Equation(rule.right, rule.left)),
                                                   right_to_left=True))
                    except ValueError:
                        raise BazaarException("The player requested an equation that is not in the games equations")
            return output

    async def request_cards(self, turn_state: TurnState) -> list[PlayerAction]:
        """
        Request card actions from the remote player based on the current turn state.

        Arguments:
            turn_state (TurnState): The current state of the turn.

        Returns:
            list[PlayerAction]: A list of player actions for card requests.
        """
        self._send([Methods.REQUEST_CARDS.name, BazaarSerializer.turn_state(turn_state)])
        try:
            return [PlayerAction(ActionType.PURCHASE_CARD,
                                 index=turn_state.tableau.index(BazaarDeserializer.card(card)))
                    for card in self._receive()]
        except ValueError:
            raise BazaarException("The player requested a card that is not in the visible cards")

    async def win(self, w: bool) -> None:
        """
        tell the remote player if they won or lost

        Arguments:
            w (bool): True if the player won, False otherwise.
        """
        self._send([Methods.WIN.name, w])
        if self._receive() == Returns.VOID:
            return
        else:
            raise BazaarException("player did not respond correctly to `win` call")

    def _send(self, message) -> None:
        """
        Send a message to the remote player.
        """
        try:
            with self.client_socket.makefile('w') as send_stream:
                send_stream.write(message)
                send_stream.flush()
        except socket.error or json.JSONDecodeError:
            raise BazaarException("message transmission failed")

    def _receive(self):
        """
        Receives and deserializes a JSON message from the connected socket.

        Raises:
            BazaarException: If a socket error occurs during data reception or if the received data is not valid JSON.
        """
        try:
            with self.socket.makefile('r') as stream:
                line = stream.readline()
                if not line:
                    raise BazaarException("Connection closed.")
                return json.loads(line.strip())
        except socket.error or json.JSONDecodeError:
            raise BazaarException("message receiving failed.")
