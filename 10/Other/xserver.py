import sys
import ijson
import argparse
import asyncio

from Bazaar.Common.JSON.deserializer import BazaarDeserializer
from Bazaar.Server.server import Server


def read_stdin():
    """
    Reads and parses JSON input from STDIN.
    """
    parser = ijson.items(sys.stdin.buffer, "", buf_size=1, multiple_values=True)

    return next(parser), next(parser)


async def main():
    """
    Main function to start the server with configurations from JSON input.
    """
    parsed = read_stdin()
    game_state = BazaarDeserializer.m10_entry(*parsed)
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    server = Server(game_state=game_state)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
