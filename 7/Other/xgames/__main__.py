import json
import sys

import ijson

from Bazaar.Common.JSON.deserializer import BazaarDeserializer
from Bazaar.Referee.referee import Referee


def read_json():
    parser = ijson.items(sys.stdin.buffer, "", buf_size=1, multiple_values=True)

    return next(parser), next(parser), next(parser)


def serialize(winner: list[str], misbehaved: list[str]) -> tuple[str, str]:
    return json.dumps(sorted(winner)), json.dumps(sorted(misbehaved))


def main() -> None:
    parsed = read_json()
    mechanisms, _, game_state = BazaarDeserializer.m8_entry(*parsed)

    referee = Referee(mechanisms, game_state)
    winner, misbehaved = serialize(*referee.play())

    sys.stdout.write(winner + "\n" + misbehaved + "\n")


if __name__ == "__main__":
    main()
