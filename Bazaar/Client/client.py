import asyncio
import socket
import json

from Bazaar.Client.player_json_interface import PlayerJsonInterface
from Bazaar.Common.JSON.deserializer import BazaarDeserializer
from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.JSON.methods import Methods
from Bazaar.Player.mechanism import PlayerMechanism


class Client:
    """
    Represents a client for connecting to and interacting with a game server.
    """
    def __init__(self, host="localhost", port=10_000, player_name="Player", player: PlayerMechanism = None):
        self.host = host
        self.port = port
        self.player_name = player_name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if player:
            self.interface = PlayerJsonInterface(player)
        self.connected = False
        self.signed_up = False

    async def connect(self):
        """
        Establishes a connection to the server using the client socket.
        """
        while not self.connected:
            try:
                print(self.host)
                print(self.port)
                self.client_socket.connect((self.host, self.port))
                self.connected = True
            except ConnectionRefusedError as e:
                continue

        await self._player_registration()
        await self._receive()
        await self._disconnect()

    async def _player_registration(self):
        self._send(json.dumps(self.player_name))

    async def _receive(self):
        """
        Continuously processes JSON requests from the server.

        Raises:
            BazaarException: If the server closes the connection.
        """
        while self.connected:
            #TODO: makefile open once
            try:
                with self.client_socket.makefile('r') as stream:
                    self.signed_up = True
                    request: json = stream.readline()
                    await self._process_request(request)
            except BazaarException:
                # server sent a malformed json, ignore the request
                pass
            except socket.error:
                self.connected = False

    async def _process_request(self, response: json) -> None:  # -> tuple[Methods, list[Equation] | TurnState | bool]:
        """
        Processes a JSON response received from the server.
        """
        message = await self._validate_json(response)
        self._send(message)

    async def _validate_json(self, response: json) -> json:
        """
        Validates and processes a JSON response from the server.

        Raises:
            BazaarException:
                - If the JSON structure is not a list of exactly two elements.
                - If the method specified in the response is invalid.
        """
        response: list = json.loads(response)
        if len(response) != 2:
            raise BazaarException("json of wrong size received.")
        try:
            method = Methods(response[0])
        except ValueError:
            raise BazaarException("Invalid method received.")
        return await self._complex(method, response[1])

    async def _complex(self, method: Methods, args: list[tuple[list[str], list[str]]] | dict[str, any] | str) -> json:
        """
        Handles complex interactions by delegating to the appropriate interface method
        based on the provided method type and arguments.

        Raises:
            BazaarException: If an invalid method type or argument is provided.
            ValueError: If the argument can not be properly deserialized.
        """
        try:
            match method:
                case Methods.SETUP:
                    equations = BazaarDeserializer.equations_to_equation_table(args)
                    message = await self.interface.setup(equations)
                case Methods.REQUEST_P_OR_T:
                    state = BazaarDeserializer.json_to_turn_state(args)
                    message = await self.interface.request_pebble_or_trades(state)
                case Methods.REQUEST_CARDS:
                    state = BazaarDeserializer.json_to_turn_state(args)
                    message = await self.interface.request_cards(state)
                case Methods.WIN:
                    message = await self.interface.win(args)
                case _:
                    raise BazaarException("Invalid method received.")
            return message
        except ValueError:
            raise BazaarException("Invalid json received.")

    def _send(self, message: json) -> None:
        with self.client_socket.makefile('w') as send_stream:
            send_stream.write(message)
            send_stream.flush()

    def _disconnect(self):
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()


if __name__ == "__main__":
    client = Client(host="localhost", port=10_000, player_name="Player1")
    asyncio.run(client.connect())
    client._disconnect()
