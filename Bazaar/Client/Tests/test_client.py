import asyncio
import json
import socket
import threading
import unittest
from unittest.mock import AsyncMock, patch
from Bazaar.Client.client import Client


class TestAsyncClient(unittest.TestCase):

    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 10_000
        self.server_thread = threading.Thread(target=self.mock_server, args=(self.host, self.port))
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        """Clean up resources after tests."""
        pass

    def mock_server(self, host="127.0.0.1", port=10_000):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Mock server running on {host}:{port}...")

        def handle_client(client_socket):
            messages = [
                json.dumps(["SETUP", {"equations": [["E1", "E2"], ["E3", "E4"]]}]),
                json.dumps(["REQUEST_P_OR_T", {"state": {"turn": 1}}]),
                json.dumps(["WIN", "Player1"]),
            ]
            try:
                for message in messages:
                    client_socket.send((message + "\n").encode())
                    asyncio.sleep(0.1)
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
            except Exception as e:
                print(f"Error in mock server: {e}")

        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()

    @patch("socket.socket")
    def test_connect_async(self, mock_socket):
        mock_socket_instance = mock_socket.return_value

        mock_socket_instance.connect = AsyncMock(return_value=None)

        mock_socket_instance.makefile.return_value.__enter__.return_value.readline.side_effect = [
            json.dumps(["SETUP", {"equations": [["E1", "E2"], ["E3", "E4"]]}]) + "\n",
            json.dumps(["REQUEST_P_OR_T", {"state": {"turn": 1}}]) + "\n",
            json.dumps(["WIN", "Player1"]) + "\n",
        ]
        client = Client(self.host, self.port, "John")
        client.client_socket = mock_socket_instance
        asyncio.run(client.connect())
        mock_socket_instance.connect.assert_called_with((self.host, self.port))


if __name__ == "__main__":
    unittest.main()
    