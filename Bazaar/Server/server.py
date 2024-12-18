import asyncio
import json
import socket
import time
from typing import Optional

from Bazaar.Common.scoring import ScoringType
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.referee import Referee
from Bazaar.Server.proxy_player import ProxyPlayer


class Server:
    """
    Represents a game server that manages client connections and initiates a multiplayer game.
    """
    host: str
    port: int
    server_socket: socket.socket
    signup_timeout: int
    name_timeout: int

    num_of_signup_periods: int
    max_signup_periods: int
    players_needed_for_game: int
    min_clients: int
    max_clients: int
    players: list[PlayerMechanism]
    default_response = str
    scoring = ScoringType
    initial_game_state: Optional[GameState] = None

    def __init__(self, host="localhost", port=10_000, scoring="NORMAL", game_state=None):
        self.host = host
        self.port = port
        self.signup_timeout = 20
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.name_timeout = 3

        self.num_of_signup_periods = 0
        self.max_signup_periods = 2
        self.players_needed_for_game = 2
        self.min_clients = 2
        self.max_clients = 6
        self.players = []
        self.default_response = json.dumps([[], []])
        self.scoring = ScoringType(scoring)
        if game_state:
            self.initial_game_state = game_state

    async def start(self) -> str:
        """
        Initiates the game process by handling the signup period and starting the game if enough players join.
        """
        self.server_socket.listen()
        await self.signup_period()

        if len(self.players) < self.players_needed_for_game:
            self.notify_failure()
            return self.default_response
        else:
            # TODO: initial_game_state.players should be the same length as players, and be fresh players
            # for player in self.players:
            #    self.initial_game_state.players.append(GamePlayer(...))
            results = Referee(self.players, self.scoring, self.initial_game_state).play()  # noqa ignoring _SpecialForm
            self.close_server()
            return json.dumps(results)

    async def signup_period(self) -> None:
        """
        Manages the player signup period, allowing clients to connect to the game server.
        """
        while self.num_of_signup_periods < self.max_signup_periods and len(self.players) < self.max_clients:
            try:
                await asyncio.wait_for(self._client_handler(), self.signup_timeout)
            except asyncio.TimeoutError:
                self.num_of_signup_periods += 1

    async def _client_handler(self) -> None:
        """
        Handles the interaction with a single client during the signup process.
        """
        start_time = time.time_ns()
        while len(self.players) < self.max_clients:
            # TODO: wrap the socket timeouts better
            try:
                self.server_socket.settimeout(start_time + self.signup_timeout - time.time_ns())
            except ValueError:
                raise asyncio.TimeoutError
            client_socket, addr = self.server_socket.accept()
            with client_socket.makefile('r') as stream:
                try:
                    loop = asyncio.get_running_loop()

                    line: json = await asyncio.wait_for(loop.run_in_executor(None, stream.readline),
                                                        min(self.name_timeout,
                                                            start_time + self.signup_timeout - time.time_ns()))
                    name = json.loads(line)
                    self.players.append(ProxyPlayer(name, client_socket))
                except asyncio.TimeoutError:
                    pass

    def notify_failure(self) -> None:
        """
        Notify the clients of a failure to start the game.
        """
        for player in self.players:
            if isinstance(player, ProxyPlayer):
                player.socket.send(self.default_response.encode())
        self.close_server()

    def close_server(self) -> None:
        """
        Shuts down the server and closes all active player connections.
        """
        self.server_socket.close()
        for player in self.players:
            if isinstance(player, ProxyPlayer):
                player.socket.shutdown(socket.SHUT_RDWR)
                player.socket.close()


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.start())
